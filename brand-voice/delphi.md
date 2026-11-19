# Delphi — Brand Voice

## Positioning

Delphi is a scoring engine for prediction markets. It ingests Polymarket
event markets, scores them on trajectory, liquidity, and maintenance-style
signals, and publishes composite 0-100 verdicts. The brand is the auditor's
lens on a noisy market: what the numbers say, what they can't say, and where
the methodology itself is the interesting finding.

## Voice in one line

*A quant reviewer who finds the structural story in the data and says plainly
when the methodology is the headline.*

## Do

- Lead with scale and distribution: "11,796 Polymarket markets scored. 8,196
  red, 3,600 yellow, zero green."
- Explain *why* the data looks the way it does (expiring markets decay on
  maintenance signals — that's structural, not a bug).
- Treat methodology self-critique as content, not weakness.
- Distinguish market odds from Delphi's health scores — never imply the
  score predicts outcomes.
- Be precise about what changed: scores, counts, time windows.

## Don't

- No financial advice, no "bet on this", no implied alpha. Ever.
- No political takes — political markets are data points, not opinions.
- No "Polymarket is rigged/broken" framing. Delphi measures signal health,
  not platform quality.
- Same banned list as gittrend: no hype words, no engagement bait.
- No outcome claims: a green score would mean healthy signals, not a likely
  resolution.

## Signature formats

- **Distribution reports**: verdict splits, score histograms, category cuts.
- **Structural findings**: "why every expiring market trends red" — the
  methodology meets market structure.
- **Movers**: score changes on live markets (currently rare — say so).
- **Coverage notes**: what got ingested, from where, when.

## UTM convention

`?utm_source=<platform>&utm_medium=social&utm_campaign=delphi-digest-<yyyymmdd>`

## Platforms

- **X / Bluesky**: distribution snapshots as text bars (e.g. `red ████████
  8196`), one link.
- **dev.to**: methodology deep dives — how do you score a market that expires?
- **Reddit**: r/polymarketmarket or quant threads only, affiliation disclosed,
  answer-first.
- **LinkedIn**: data-engineering angle — scoring 2.35M observations nightly.
