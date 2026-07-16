# OPS-2214 (repaired via /harness-issues Mode B; posted back to the ticket)

## ISSUE — Statement interest matches the ledger to the cent for every account

Context: Statement interest differs from the core ledger by −2 to +3 cents for
~0.4% of accounts monthly because stmtgen rounds each daily accrual line HALF_UP
before summing, while the ledger rounds once at month-end HALF_EVEN per group
accounting policy. Ops writes off the differences manually each cycle, and internal
audit has raised a finding about the recurring write-offs.
Source: b.naidoo (Ops Reconciliation), OPS-2214.
Requirement refs: this ticket (fast path — OPS-2214 is the ID).
Depends on: nothing.
Linked records: AUD-2026-041 (internal audit finding this fix remediates).

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| UI | none — statement PDF values change as a consequence, no template change |
| API contract | none — figures only |
| Backend (stmtgen, Java 8) | AccrualAggregator rounding: aggregate-then-round HALF_EVEN |
| Data | none — no schema change |
| Deploy/config | code only |

(Justified near-horizontal slice: the behavior is numeric correctness surfacing in
existing statements.)

### Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| 1 | Given the masked replay set for the last closed cycle, when statements regenerate in test, then every interest line equals the ledger figure to the cent |
| 2 | Given the known drift accounts from the recon set, when regenerated, then prior −2..+3c differences are all zero |
| 3 | Given accounts with zero prior drift, when regenerated, then their figures are unchanged |

### Proof

```bash
./gradlew statementReplayTest --cycle 2026-06   # expect: 0 mismatches vs ledger
```

### Out of scope

Accrual methodology, day-count conventions, ledger-side changes, statement layout,
back-dated correction of already-issued statements (disposition decided in the
change record, not silently here).

### Definition of Ready

- [x] Behavior title · [x] fresh-session test · [x] slice table (exception noted)
- [x] testable criteria · [x] proof command · [x] out-of-scope · [x] sized ≤ 1 day code + recon
