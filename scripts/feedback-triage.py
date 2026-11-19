#!/usr/bin/env python3
"""Daily feedback triage pass for the lucanian.app fleet.

Reads new (untriaged) submissions from the feedback service SQLite DB
(read-only), classifies them, auto-files confident bugs as GitHub issues,
and stages author reply drafts into the Kevin-approval queue.

Contract with the w2 feedback service (Rust, SQLite): a table named
`submissions` with at least:
    id TEXT PRIMARY KEY
    product TEXT          -- gittrend | delphi | ... (may be NULL)
    source TEXT           -- where the submission came from
    author TEXT           -- email/handle (may be NULL)
    content TEXT NOT NULL
    created_at TEXT
Triage writes back (same table): classification, sentiment, confidence,
triaged_at, github_issue_url, theme. The service may add columns freely.

Usage: feedback-triage.py [--digest]   # --digest = weekly Friday digest mode
Env:   FEEDBACK_DB (path; skip silently if unset/missing)
       FEEDBACK_DRY_RUN=1 (classify and print, file nothing)
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
import datetime

DB_PATH = os.environ.get("FEEDBACK_DB", "/var/lib/feedback/feedback.db")
DRY_RUN = os.environ.get("FEEDBACK_DRY_RUN") == "1"
MARKETING = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE_DIR = os.path.join(MARKETING, "drafts", "feedback-replies")
REPORTS_DIR = os.path.join(MARKETING, "reports")

# product name -> github repo (only repos we may file against)
PRODUCT_REPOS = {
    "gittrend": "kevincouton/gittrend",
    "delphi": "kevincouton/delphi",
    "finroadmap": "kevincouton/finroadmap",
    "fablayer": "kevincouton/fablayer",
    "marketplace": "kevincouton/marketplace",
    "risk": "kevincouton/risk",
    "handbook": "kevincouton/handbook",
}

PRODUCT_WORDS = {
    "gittrend": ["gittrend", "git trend", "gittrend.lucanian.app"],
    "delphi": ["delphi", "delphi.lucanian.app"],
    "finroadmap": ["finroadmap", "fin roadmap"],
    "fablayer": ["fablayer", "fab layer"],
    "marketplace": ["marketplace.lucanian.app"],
    "risk": ["risk.lucanian.app"],
    "handbook": ["handbook", "handbookhub"],
}

BUG_WORDS = [
    "broken", "bug", "crash", "doesn't work", "does not work", "dont work",
    "doesn't load", "404", "500", "error", "failed", "fails", "blank page",
    "white screen", "wrong", "incorrect", "stale", "outdated", "slow",
    "timeout", "hangs", "freezes", "regression",
]
FEATURE_WORDS = [
    "feature request", "please add", "would be nice", "wish", "suggestion",
    "could you add", "it would be great", "i'd love", "can you add",
    "support for", "filter by", "sort by", "export", "rss", "digest",
    "weekly email", "api", "webhook", "badge",
]
PRAISE_WORDS = [
    "thanks", "thank you", "great", "love", "awesome", "amazing", "useful",
    "helpful", "nice work", "well done", "impressive", "exactly what",
]
SPAM_WORDS = [
    "seo services", "crypto", "airdrop", "promote your", "marketing agency",
    "buy followers", "casino", "viagra", "cbd gummies", "guest post",
]
NEGATIVE_WORDS = BUG_WORDS + ["disappointed", "frustrating", "annoying", "terrible", "awful"]
POSITIVE_WORDS = PRAISE_WORDS

CLASS_CONFIDENCE = {"bug": 0.75, "feature": 0.7, "praise": 0.8, "spam": 0.85}

THEME_BUCKETS = {
    "digest & notifications": ["digest", "weekly email", "newsletter", "notify"],
    "badges & embeds": ["badge", "embed", "shield"],
    "api & integrations": ["api", "webhook", "graphql", "integration"],
    "search & filters": ["search", "filter", "sort"],
    "exports & data": ["export", "csv", "download", "dataset"],
}


def theme_of(content: str) -> str:
    text = content.lower()
    for theme, words in THEME_BUCKETS.items():
        if any(w in text for w in words):
            return theme
    return "other"


def classify(content: str, product: str | None):
    text = content.lower()
    links = len(re.findall(r"https?://", text))
    hits = lambda words: sum(1 for w in words if w in text)

    spam_score = hits(SPAM_WORDS) * 3 + (2 if links >= 3 and len(text) < 300 else 0)
    bug_score = hits(BUG_WORDS)
    feature_score = hits(FEATURE_WORDS)
    praise_score = hits(PRAISE_WORDS)

    if spam_score >= 3:
        klass, why = "spam", f"spam signals ({spam_score})"
    elif bug_score and not feature_score:
        klass, why = "bug", f"bug words x{bug_score}"
    elif praise_score > feature_score and not bug_score:
        klass, why = "praise", f"praise words x{praise_score} outweigh feature words x{feature_score}"
    elif feature_score and not bug_score:
        klass, why = "feature", f"feature words x{feature_score}"
    elif praise_score and not (bug_score or feature_score):
        klass, why = "praise", f"praise words x{praise_score}"
    elif bug_score > feature_score:
        klass, why = "bug", f"more bug ({bug_score}) than feature ({feature_score}) signals"
    elif feature_score:
        klass, why = "feature", "mixed signals, leaning feature"
    else:
        klass, why = "other", "no strong signals — needs Kevin"

    if klass in CLASS_CONFIDENCE:
        confidence = CLASS_CONFIDENCE[klass]
        if max(bug_score, feature_score, praise_score) >= 2:
            confidence = min(0.95, confidence + 0.1)
    else:
        confidence = 0.0

    if hits(NEGATIVE_WORDS):
        sentiment = "negative"
    elif hits(POSITIVE_WORDS):
        sentiment = "positive"
    else:
        sentiment = "neutral"

    if not product:
        for name, words in PRODUCT_WORDS.items():
            if any(w in text for w in words):
                product = name
                break
    return klass, sentiment, round(confidence, 2), product, why


def file_bug(sub, repo: str) -> str | None:
    """Create a GitHub issue; return its URL. Idempotent per submission id."""
    marker = f"feedback-{sub['id'][:8]}"
    search = subprocess.run(
        ["gh", "search", "issues", marker, "--repo", repo, "--state", "open",
         "--json", "number", "-L", "1"],
        capture_output=True, text=True)
    try:
        if json.loads(search.stdout or "[]"):
            return "already-filed"
    except json.JSONDecodeError:
        pass

    title = f"[feedback] {sub['content'].strip().splitlines()[0][:70]}"
    body = f"""Submitted via: {sub.get('source') or 'unknown'}
Author: {sub.get('author') or 'anonymous'}
Submitted at: {sub.get('created_at') or 'unknown'}
Submission id: {marker}

> {sub['content'].strip()}

---
Auto-filed by the feedback triage pass (classification: bug, confidence {sub.get('confidence')}).
Please edit the title/body into a proper bug report as needed.
Reproduction context to gather: product, page/route, browser, time."""
    r = subprocess.run(
        ["gh", "issue", "create", "--repo", repo, "--title", title,
         "--body", body, "--label", "feedback"],
        capture_output=True, text=True)
    url = r.stdout.strip()
    return url if url.startswith("http") else None


def main():
    digest_mode = "--digest" in sys.argv
    if not os.path.exists(DB_PATH):
        print(f"feedback DB not present at {DB_PATH} — nothing to triage")
        return 0

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    # Best-effort: ensure triage columns exist (service may pre-create them).
    for col, decl in [
        ("classification", "TEXT"), ("sentiment", "TEXT"), ("confidence", "REAL"),
        ("triaged_at", "TEXT"), ("github_issue_url", "TEXT"), ("theme", "TEXT"),
    ]:
        try:
            cur.execute(f"ALTER TABLE submissions ADD COLUMN {col} {decl}")
        except sqlite3.OperationalError:
            pass
    con.commit()

    if not digest_mode:
        rows = cur.execute(
            "SELECT * FROM submissions WHERE classification IS NULL"
        ).fetchall()
        filed, drafted = 0, 0
        for row in rows:
            sub = dict(row)
            klass, sentiment, conf, product, why = classify(
                sub["content"], sub.get("product"))
            print(f"[{klass} {conf}] ({product or '?'}/{sentiment}) {why}: "
                  f"{sub['content'][:80]!r}")
            if DRY_RUN:
                continue
            issue_url = None
            if klass == "bug" and conf >= 0.7 and product in PRODUCT_REPOS:
                issue_url = file_bug({**sub, "confidence": conf}, PRODUCT_REPOS[product])
                if issue_url == "already-filed":
                    issue_url = None
                elif issue_url:
                    filed += 1
            # reply drafts for everything except spam go to Kevin's queue
            if klass != "spam":
                os.makedirs(QUEUE_DIR, exist_ok=True)
                slug = re.sub(r"[^a-z0-9]+", "-", sub["content"][:40].lower()).strip("-")
                with open(os.path.join(QUEUE_DIR, f"pending-{sub['id'][:8]}-{slug}.md"), "w") as f:
                    f.write(f"<!-- Kevin approves before anything is sent. "
                            f"Classification: {klass}/{sentiment} (conf {conf}). -->\n\n")
                drafted += 1
            theme = theme_of(sub["content"]) if klass == "feature" else None
            try:
                cur.execute(
                    "UPDATE submissions SET classification=?, sentiment=?, confidence=?, "
                    "product=COALESCE(product, ?), triaged_at=?, github_issue_url=?, theme=? WHERE id=?",
                    (klass, sentiment, conf, product,
                     datetime.datetime.now(datetime.timezone.utc).isoformat(), issue_url, theme, sub["id"]))
            except sqlite3.Error as e:
                print(f"  (write-back skipped: {e})")
        con.commit()
        print(f"triage complete: {len(rows)} processed, {filed} bugs filed, {drafted} reply drafts queued")
        return 0

    # ---- weekly digest ----
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=7)).isoformat()
    week = cur.execute(
        "SELECT classification, count(*) FROM submissions WHERE triaged_at >= ? GROUP BY 1",
        (since,)).fetchall()
    themes_rows = cur.execute(
        "SELECT theme, count(*) c FROM submissions WHERE classification='feature' "
        "AND triaged_at >= ? GROUP BY theme ORDER BY c DESC LIMIT 10", (since,)).fetchall()
    bugs = cur.execute(
        "SELECT product, content, github_issue_url FROM submissions "
        "WHERE classification='bug' AND triaged_at >= ? ORDER BY triaged_at", (since,)).fetchall()
    praise = cur.execute(
        "SELECT content FROM submissions WHERE classification='praise' "
        "AND triaged_at >= ? ORDER BY triaged_at LIMIT 5", (since,)).fetchall()

    os.makedirs(REPORTS_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()
    path = os.path.join(REPORTS_DIR, f"feedback-digest-{today}.md")
    with open(path, "w") as f:
        f.write(f"# Feedback digest — week ending {today}\n\n")
        f.write("## Volume by classification\n\n")
        for k, c in week:
            f.write(f"- {k}: {c}\n")
        f.write("\n## Top feature themes\n\n")
        for t, c in themes_rows:
            f.write(f"- {t or '(untagged)'}: {c}\n")
        f.write("\n## Bugs auto-filed\n\n")
        for b in bugs:
            link = b["github_issue_url"] or "(not filed — low confidence or unmapped product)"
            f.write(f"- [{b['product'] or '?'}] {b['content'][:100]} → {link}\n")
        f.write("\n## Praise highlights\n\n")
        for p in praise:
            f.write(f"> {p['content'][:200]}\n\n")
        f.write("\n## Fixed from prior feedback\n\n")
        f.write("_Cross-reference closed issues labeled `feedback` since the last "
                 "digest — fill in from `gh issue list --repo ... --label feedback --state closed`._\n")
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
