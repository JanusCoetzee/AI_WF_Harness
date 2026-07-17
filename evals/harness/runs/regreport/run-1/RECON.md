# RECON — REG-9034

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Fall-through defect | liqreport/rules/deposit_classes.py:142 | `partner_program_id` present on the account record but never consulted; partner deposits land in "stable retail" |
| Rule entry point | deposit_classes.py:57 `classify()` | pure function of account record — good seam for period-versioned rules |
| Period context | liqreport/run.py:88 | reporting period already threaded to the generator — rule selection can key off it |
| Archived returns | portal archive + rule-code version recorded per period | replay of prior periods is possible |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| Regulator portal return | the report itself | run.py:120 |
| ALCO liquidity dashboard | reads the same classified feed nightly | grep + t.okafor |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| ALCO dashboard buckets by the same class labels | dashboard query uses class strings | Ruling: labels unchanged, membership shifts — ALCO informed; their trend lines will step at 2026-10 (annotated) |
| 2026-09 period must reproduce old behavior post-deploy | RI-2026-07 effective by reporting period | This is REG-9034.2 — pinned |

## Test coverage reality

- Existing tests: classify() unit tests for current classes; no partner-flag cases.
- **Characterization tests added:** classify() outputs pinned for a masked 50k-account
  sample under current rules — including the wrong partner-flag fall-throughs
  (deliberately pinned; the change commit moves them visibly). Replay harness
  regenerates prior periods; misstatement quantified: 0.6–0.9pp per quarter over
  5 quarters.
- Masked data only.

## Surprises / archaeology

| Finding | Action |
| --- | --- |
| Operational corporate accounts with partner flags also fall through — submitted returns affected for 5 quarters | Escalated to Driver + t.okafor same day; remediation section of CHANGE.md owns disposition |

## Revised blast radius & tier

ALCO dashboard added as consumer; tier stays T1; triggers re-answered — no new trips.

## Go / No-go

- [x] Blast radius confirmed
- [x] Characterization tests green against unchanged code; prior-period impact quantified
- [x] Triggers re-checked after the operational-accounts discovery
- **Recommendation:** go — gated on t.okafor's remediation ruling before first corrected submission
