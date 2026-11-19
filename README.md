# Lucanian Agent Marketing Agency

An agent-run, Kevin-approved marketing operation for the lucanian.app product
fleet (GitTrend, Delphi, and siblings). The agency produces data-backed
editorial content about what the data actually shows — no hype, no
astroturfing, nothing published without Kevin's explicit approval.

## Roles

| Role | Agent | Responsibility |
| --- | --- | --- |
| Editor-in-chief | main agent | Owns the calendar, approves story angles, quality-bars every draft, reports to Kevin. |
| Data journalist | main agent | Queries production DBs (read-only) for story evidence: movers, verdict shifts, anomalies, distributions. Every claim in a draft traces to a query. |
| Copywriter | main agent | Turns the evidence into platform-native drafts (X, Bluesky, dev.to, Reddit, LinkedIn). |
| Visual producer | main agent | Charts (matplotlib), screenshots (Playwright), OG images for long-form. |
| Distribution ops | Kevin | Posts approved drafts from his own accounts. Agents never hold posting credentials. |
| Analyst | main agent | Weekly attribution report: UTM traffic (Umami), engagement, what moved. |

## Weekly loop

- **Mon — data scan.** Query each product DB for the week's story candidates
  (movers, verdict changes, new entries, anomalies). Produce a shortlist with
  evidence attached.
- **Tue — draft pack.** 10–15 drafts with evidence, UTM links, and visuals
  where they earn their place. Delivered to Kevin for review.
- **Wed–Sun — scheduled posting.** Kevin posts (or approves scheduling) the
  approved drafts at the slots on the editorial calendar. The agency is on
  watch for replies and questions on posted threads.
- **Fri — analyst report.** Attributed traffic per channel/piece, top
  referrers, conversion to repo clicks or signups, and next week's
  recommendations. Saved under `reports/`.

## Guardrails (hard rules)

1. **Nothing posts without Kevin's approval.** Every draft is a file Kevin
   reviews; he posts from his own accounts. No exceptions, no auto-posting.
2. **No astroturfing.** No fake accounts, no vote rings, no "my friend built
   this" posts about our own products, no undisclosed self-promotion on
   Reddit. Reddit participation is a real community member account disclosing
   affiliation when relevant.
3. **Platform rules respected.** One Show HN per product, ever. No repost
   spam. Follow each subreddit's self-promotion ratio. X/Bluesky: no hashtag
   stuffing, no reply-guy automation.
4. **Kill criteria.** Any channel with **zero attributed results after 4
   weeks** (UTM sessions, meaningful engagement, or inbound) is paused and
   its budget of drafts reallocated. Reported in the Friday analyst report.
5. **Evidence or it didn't happen.** Every number in a draft must come from a
   recorded query against the production DB (or the product itself). No
   invented stats, no "industry-leading" claims.
6. **Read-only against production.** Marketing work never writes to product
   databases and never touches production infra.

## House voice

Across products: plain, numbers-first, slightly wry. We show the query and
the finding. We never say "revolutionary", "game-changing", or "unlock".
Product-specific voice lives in `brand-voice/`.

## Repo layout

```
brand-voice/   per-product voice guides
calendar/      weekly editorial calendars (YYYY-Www.md)
drafts/        draft packs, pending and approved
assets/        charts, screenshots, og images
reports/       weekly analyst reports
```
