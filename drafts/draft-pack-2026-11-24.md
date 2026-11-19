# Draft pack — week of Nov 24, 2026

12 drafts. Every number traces to a query listed under **Evidence**.
Nothing here is approved or posted until Kevin says so.
UTM base: `https://gittrend.lucanian.app/` / `https://delphi.lucanian.app/`.

---

## GT-1 · X — weekly movers (FLAGSHIP)

**Asset:** `../assets/week-2026-11-24/gittrend-movers.png`

**Draft:**

> We score 4,185 open-source repos every week. Top movers this week:
>
> · OpenBB-finance/OpenBB 54 → 89
> · github/copilot-sdk 52 → 87
> · Kludex/uvicorn 56 → 88
> · Data-Centric-AI-Community/fg-data-profiling 49 → 84
> · NicolasHug/Surprise 38 → 73
>
> Scores blend release velocity, contributor concentration, issue
> responsiveness, and docs quality. Full methodology:
> https://gittrend.lucanian.app/roadmap?utm_source=x&utm_medium=social&utm_campaign=weekly-movers-20261124

**Evidence:** gittrend.db — latest vs previous `gittrend_score` per repo,
top gains (query in git history of this file's repo: `assets/week-2026-11-24`).

---

## GT-2 · Bluesky — weekly movers (text variant)

> top movers on GitTrend this week (of 4,185 repos scored):
> OpenBB 54→89, copilot-sdk 52→87, uvicorn 56→88, fg-data-profiling 49→84, Surprise 38→73
> what moved: release cadence + docs, mostly. scores recompute on a timer, no manual nudges
> https://gittrend.lucanian.app/?utm_source=bluesky&utm_medium=social&utm_campaign=weekly-movers-20261124

**Evidence:** same query as GT-1.

---

## GT-3 · dev.to — methodology deep dive

**Title:** How GitTrend scores 4,185 repos (and why stars aren't the score)

**Body (outline, ~900 words):**
1. The problem: stars measure fame, not maintenance. A repo with 60k stars
   and a 3-year issue backlog.
2. The four signal families: release velocity, contributor concentration
   (Gini), issue resolution median, docs quality (quickstart minutes, API
   coverage, runnable examples). Each 0-100, blended into the GitTrend Score.
3. Verdicts: green 80+, yellow 50-79, red <50, critical.
4. Distribution right now: 886 green, 678 yellow, 1,069 red, 86 critical
   (latest score per repo).
5. Limits, honestly: score measures maintenance signals, not code quality;
   young repos are penalized on velocity; awesome-lists score structurally
   low (see GT-7).
6. The stack: Rust collectors, SQLite, the whole pipeline is open source:
   https://github.com/kevincouton/gittrend
7. CTA with UTM.

**Assets:** gittrend-lang-avg.png optional; verdict counts table.

**Evidence:** verdict distribution query against gittrend.db (latest rn=1):
critical 86 / green 886 / red 1,069 / yellow 678.

---

## GT-4 · LinkedIn — engineering-culture angle

> We replaced "how many stars does it have?" with "what's its score?" in our
> own dependency reviews.
>
> GitTrend scores 4,185 open-source repos on release velocity, contributor
> concentration, issue responsiveness, and documentation quality — then shows
> the number next to the repo. The uncomfortable finding: TypeScript repos
> average 76.5/100. Rust averages 59.5. Popularity and maintenance are
> different axes.
>
> Full methodology: https://gittrend.lucanian.app/roadmap?utm_source=linkedin&utm_medium=social&utm_campaign=gittrend-methodology-20261125

**Evidence:** language-average query (n=202 TS, 748 Rust, 527 Python, 372 Go).

---

## GT-5 · X — language averages (chart)

**Asset:** `../assets/week-2026-11-24/gittrend-lang-avg.png`

> Average GitTrend Score by language (latest score per repo, n in chart).
> TypeScript leads. Rust — the most-tracked language on the platform (1,379
> repos) — averages 59.5.
> Maintenance signals ≠ hype. Methodology:
> https://gittrend.lucanian.app/roadmap?utm_source=x&utm_medium=social&utm_campaign=lang-scores-20261126

**Evidence:** language-average query; repos.language counts (Rust 1,379).

---

## GT-6 · Bluesky — language text-bars

> avg GitTrend Score by language:
> TypeScript 76.5 ██████████████▎
> Python     71.0 █████████████▏
> Rust       59.5 ███████████▏
> Go         57.5 ██████████▊
> (n = 202 / 527 / 1,379 / 372; latest score per repo)
> 4,185 repos scored → https://gittrend.lucanian.app/?utm_source=bluesky&utm_medium=social&utm_campaign=lang-scores-20261126

**Evidence:** same as GT-5.

---

## GT-7 · dev.to — the awesome-list penalty

**Title:** The highest-starred repos with the worst scores are all awesome-lists

**Body (outline, ~700 words):**
1. Query: latest-score repos with verdict=critical, sorted by stars. Top:
   agarrharr/awesome-macos-screensavers (4,368★, score 29),
   caesar0301/awesome-pcaptools (3,390★, 27),
   brootware/awesome-cyber-security-university (3,050★, 26),
   ttt30ga/awesome-product-design (2,607★, 25), NARKOZ/guides (2,403★, 25).
2. Why: the methodology scores maintenance — releases, issue flow, docs.
   Curated lists have none of that machinery. The score is *correct*: an
   awesome-list is not a maintained piece of software.
3. The takeaway: star counts and maintainability diverge hard on doc-style
   repos. Pick your signal for the job.
4. Verdict colors explained + link with UTM.

**Evidence:** critical-with-stars query (top 6 rows listed above).

---

## DP-1 · X — verdict distribution snapshot

**Asset:** `../assets/week-2026-11-24/delphi-verdicts.png`

> We scored 11,796 Polymarket markets. 8,196 red. 3,600 yellow. Zero green.
> This is a finding about market structure, not market odds — expiring
> markets decay on maintenance signals. How the scoring works:
> https://delphi.lucanian.app/?utm_source=x&utm_medium=social&utm_campaign=delphi-digest-20261123

**Evidence:** delphi.db latest-verdict counts (red 8,196 / yellow 3,600 / no
green or critical rows).

---

## DP-2 · Bluesky — "zero green" text-bar

> Delphi has now scored 11,796 prediction markets:
> red    8196 ████████████████▎
> yellow 3600 ███████▏
> green     0
> why zero: event markets expire, and expired things score like unmaintained
> things. structural, not a bug. →
> https://delphi.lucanian.app/?utm_source=bluesky&utm_medium=social&utm_campaign=delphi-digest-20261123

**Evidence:** same as DP-1.

---

## DP-3 · LinkedIn — data-engineering angle

> What does it take to keep 2.35M quality observations fresh on 11,796
> prediction markets?
>
> Our Delphi pipeline ingests Polymarket markets, scores each on trajectory
> and liquidity-style signals, and stores every observation — 2.35M rows and
> counting — so any verdict can be traced back through time. The API serves
> the latest snapshot in ~30ms (stats cached with a 60s TTL; cold recompute
> is 2.4s over the full table).
>
> Rust + SQLite + a six-hour ingest timer. Details:
> https://delphi.lucanian.app/?utm_source=linkedin&utm_medium=social&utm_campaign=delphi-engineering-20261124

**Evidence:** entity_scores count 2,350,859; entities 11,796; stats latency
measured 2026-11-19 (35ms warm / 2.4s cold, pre/post cache deploy).

---

## DP-4 · dev.to — scoring markets that expire

**Title:** How do you score a prediction market that expires? (Delphi methodology)

**Body (outline, ~1,000 words):**
1. Prediction markets are events, not software — but maintenance-style
   signals still apply: is the market active, resolving, liquid?
2. What Delphi ingests (Polymarket), what it stores (every observation).
3. The structural finding: 100% of scored markets land red/yellow. A market
   past resolution date has no active signals — it reads as "unmaintained".
   The score describes signal health, not outcome probability. These are
   different things and conflating them is the #1 misread.
4. Composite 0-100, verdict bands, full traceability.
5. What we'd need for a fairer "expired market" scoring — open question,
   genuinely inviting comments.
6. UTM link.

**Evidence:** latest-verdict counts; stats endpoint; schema notes.

---

## GT-8 · Reddit — reactive thread reply (HOLD)

**Precondition:** a thread in r/opensource / r/rust / r/Python where repo
quality ranking is genuinely on-topic. Disclose affiliation in the reply.

> Affiliation: I run GitTrend (scored repo directory). The "stars vs
> maintenance" question comes up a lot — we score ~4.2k repos on release
> velocity, contributor concentration, issue responsiveness, and docs. The
> pattern in this thread matches what the data says: [relevant 1-2 sentence
> finding]. Methodology if useful:
> https://gittrend.lucanian.app/roadmap?utm_source=reddit&utm_medium=social&utm_campaign=reddit-quality-20261129

**Evidence:** language/verdict/movers queries as relevant to the thread.
