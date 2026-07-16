# ADR-001 — Round interest once at aggregation, HALF_EVEN, aligning stmtgen to ledger policy

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-17 |
| Deciders | janus + Finance representative (drill placeholder) |
| REQs served | OPS-2214.1-.3 |

## Context

stmtgen rounds each daily accrual HALF_UP at line level (undocumented, predates
team) then sums; the ledger accrues unrounded and rounds once at month-end
HALF_EVEN per group accounting policy. This ADR documents the status quo it
supersedes (retro-ADR duty) and the change.

## Options considered

### Option A — sum unrounded dailies, round once at aggregate, HALF_EVEN

- Pros: exactly matches ledger policy and figures; smallest diff; policy-documented.
- Cons: daily-annex display values no longer sum visibly to the total (display
  rounding vs computed total) — annex keeps display-only rounding, footnoted.

### Option B — keep line-level rounding but switch it to HALF_EVEN

- Pros: annex sums visually.
- Cons: still drifts from the ledger (rounding early ≠ rounding once); fails the
  actual requirement. Rejected on arithmetic, not taste.

### Option C — leave code, automate the write-off journal

- Pros: no statement change; tax feed untouched.
- Cons: institutionalizes figures that don't match the ledger; audit finding stays
  open; tax feed keeps reporting drifted values. The do-nothing steelman, honestly
  weighed and rejected.

## Decision

Option A. Discriminating reason: the ledger's round-once HALF_EVEN is documented
group accounting policy; statements must report the policy figure.

## Consequences

Ops write-off journal retires. Tax feed values shift by cents going forward —
Finance ruling governs prior-year handling. Tripwire: any future consumer needing
line-level rounded aggregates must trigger a new ADR, not a quiet revert.
