# RECON — OPS-2214

Every claim cites file:line (paths are scenario facts) or a test.

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Defect site | src/main/java/com/bank/stmtgen/accrual/AccrualAggregator.java:214 | `daily.setScale(2, RoundingMode.HALF_UP)` per line, then sum at :231 |
| Ledger policy reference | group accounting policy: round once at month-end, HALF_EVEN | confirmed with Finance |
| Statement assembly | StatementComposer.java:88 | consumes aggregate, no re-rounding |
| Config/flags altering path | none — rounding is hardcoded | |

## Consumers found

| Consumer | How it depends on touched behavior | Found via |
| --- | --- | --- |
| Customer PDF statements | prints the aggregate interest figure | StatementComposer.java:88 |
| GL reconciliation export | ReconExportJob.java:141 exports the statement figure; Ops journal writes off the delta vs ledger monthly | grep + b.naidoo |
| **Tax-reporting feed** | TaxFeedBuilder.java:97 uses the *statement* figure, not the ledger figure — the annual feed has been reporting the drifted number | grep — surprise consumer |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| Ops recon journal expects a small nonzero write-off each cycle | ReconExportJob.java:141 + ops runbook | Human ruling: yes — eliminating the write-off is the point; ops informed, journal step retires |
| Tax feed values historically equal statement (drifted) values | TaxFeedBuilder.java:97 | **Human ruling required** — post-fix, tax feed values change by cents; prior-year feeds already submitted with drifted figures. Flagged to Driver/Finance — this is why the tier is T1 |
| Per-line rounded values appear in the daily-accrual detail annex on some statement styles | StatementComposer.java:129 | Ruling: keep per-line display rounding for the annex; fix the aggregate only |

## Test coverage reality

- Existing tests: AccrualAggregatorTest covers happy path at line level only.
- **Characterization tests added:** replay harness pins current aggregate outputs
  (including the wrong ones) for a masked 10k-account sample; drift distribution
  −2..+3c reproduced exactly. Data: masked/synthetic only.
- Left unpinned: PDF byte layout (composer untouched).

## Surprises / archaeology

| Finding | Action |
| --- | --- |
| HALF_UP at line level is undocumented and predates the team | Retro-ADR written as part of adr/ADR-001-rounding.md (status quo + change) |
| Tax feed consumes statement figure | escalated to Driver; Finance consult before build |

## Revised blast radius & tier

Blast radius grows: tax feed added as consumer. Tier stays T1 (already assumed
worst). Escalation triggers re-checked: trigger 2 already Yes (ADR done); no new
trips.

## Go / No-go

- [x] Blast radius confirmed, no unknowns
- [x] Characterization tests green against unchanged code (drift reproduced)
- [x] Triggers re-checked
- **Recommendation:** go, gated on Finance ruling for the tax-feed value shift
