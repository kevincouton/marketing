# Feedback triage loop

A daily, server-side pass over user feedback submissions for the lucanian.app
fleet. Built against the feedback service that w2 owns (Rust + SQLite); this
document is the contract between the service and the triage pass.

## Flow

```
submissions (feedback service DB)
        │  daily 06:20 CET — feedback-triage.timer
        ▼
feedback-triage.py
  1. Load submissions WHERE classification IS NULL
  2. Classify: bug | feature | praise | spam | other, + sentiment
     (positive/neutral/negative), + product tag, + confidence
  3. bug & confidence ≥ 0.70 & known product → GitHub issue in the product
     repo (label: feedback, body carries source/author/time/submission id)
  4. Everything except spam → author reply DRAFT in
     drafts/feedback-replies/  ← Kevin-approval queue; nothing sends itself
  5. Write-back: classification, sentiment, confidence, product, theme,
     triaged_at, github_issue_url (best-effort; missing columns are added)
        │
        │  Fridays 16:30 CET — feedback-digest.timer
        ▼
weekly digest → reports/feedback-digest-YYYY-MM-DD.md
  - volume by classification
  - top feature themes (clustered buckets)
  - bugs filed with issue links
  - praise highlights
  - "fixed from prior feedback": cross-reference of closed issues labeled
    feedback since the last digest
  - committed and pushed to the marketing repo automatically
```

## DB contract (w2 service ↔ triage pass)

Table `submissions`; the service may add columns, the pass adds its own if
absent:

| column | set by | notes |
| --- | --- | --- |
| id, content, created_at | service | required |
| product, source, author | service | product may be NULL — pass infers from content |
| classification, sentiment, confidence | triage | bug/feature/praise/spam/other |
| theme | triage | feature clustering: digest & notifications, badges & embeds, api & integrations, search & filters, exports & data, other |
| triaged_at, github_issue_url | triage | |

DB path: `FEEDBACK_DB` env (systemd unit sets
`/var/lib/feedback/feedback.db`; the pass exits silently if absent).

## Rules

- Classification is transparent keyword scoring, not a black box. Anything
  classified `other` (no strong signals) goes to Kevin, not to GitHub.
- Bugs are only auto-filed for products in the repo map (gittrend, delphi,
  finroadmap, fablayer, marketplace, risk, handbook). Unknown product → no
  filing, flagged in output.
- Filing is idempotent: each submission id is embedded in the issue body as
  `feedback-<id>` and searched before creating.
- **Reply drafts are drafts.** Sending any reply to a human requires Kevin's
  explicit approval, same as every other public-facing artifact.
- Spam is recorded (counts feed the digest) and otherwise dropped.

## Ops

- Timers: `feedback-triage.timer` (daily 06:20), `feedback-digest.timer`
  (Fri 16:30). Check: `systemctl list-timers feedback-*`.
- Manual run: `FEEDBACK_DB=/path/to.db python3 scripts/feedback-triage.py`
  (add `--digest` for the weekly digest; `FEEDBACK_DRY_RUN=1` to classify
  without writing or filing).
- Logs: `journalctl -u feedback-triage.service`.
