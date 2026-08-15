# CHANGE — GH-19 audit-decisions.sh doesn't check DECISIONS.log chronology

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #19 — found during independent re-verification of GH-16, 2026-08-12 |
| Date | 2026-08-12 |
| Risk tier | T2 — internal governance tooling; runs inside `verify.sh`'s lint step (`harness.config.yaml`), so a defect here is CI-visible, but touches no customer data or external interface |
| Recon | waived-trivial (additive check appended to an existing, well-understood script; no existing behavior changed — see RECON below for the one thing worth citing) |
| Linked records | the GH-16 misdated/out-of-order `DECISIONS.log` entry this generalizes from (fixed in commit `b770563`) |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop — mechanical, cheap checks belong in the loop, not left to a human reading raw files), §5 (traceability — the log's value is being a trustworthy, ordered audit trail) |

## Intent

`audit-decisions.sh` cross-checks claims *against* `DECISIONS.log` but never
checked the log's own internal consistency. A session working GH-16 appended
an entry dated `2026-08-11` sandwiched between two `2026-08-12` entries —
wrong date, out of order — and `verify.sh` stayed green throughout; a human
had to read the raw file to find it. Done means a non-decreasing-date check
runs automatically as part of `audit-decisions.sh` (already chained into
`verify.sh`'s lint step).

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-19.1 | Given `DECISIONS.log` with a line dated earlier than the line before it, when `audit-decisions.sh` runs, then it fails and reports the file:line, the offending date, and the two adjacent entries |
| GH-19.2 | Given `DECISIONS.log` as it exists today (dates non-decreasing throughout), when `audit-decisions.sh` runs, then the new check passes and existing checks 1-4 are unaffected |
| GH-19.3 | The check parses only the leading `YYYY-MM-DD` token per line (lines without one, e.g. continuation text, are skipped rather than false-failing) |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/audit-decisions.sh` only (new section 5, appended; sections 1-4 untouched) |
| Known consumers | `scripts/verify.sh` lint step (every verify run, local + CI); humans running the script directly |
| Data elements | none — reads local markdown, Internal at most |
| Deploy surface | script only |

## Rollback note

Revert the commit. The new section is purely additive (no existing check's
logic or output format changed), so rollback has zero migration surface.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — same `require_line`-style pattern of "scan a file, count FAILS, report" already used by sections 1-4 | ADR |
| Effort beyond ~3 days after recon? | No — under an hour | G1 |
| Tier raised during recon? | No | re-approve |

## Verification (manual — no test harness for this bash script)

```
$ bash scripts/audit-decisions.sh          # clean run
  ✓ docs/harness/DECISIONS.log dates are non-decreasing
audit-decisions: all claims logged.
$ echo 'EXIT: 0'

# injected an out-of-order 2026-08-11 line between two 2026-08-12 lines:
  ✗ OUT OF ORDER: docs/harness/DECISIONS.log:73 dated 2026-08-11 comes after a 2026-08-12 entry
      prior: 2026-08-12 | note | janus | opened #16: ...
      this:  2026-08-11 | note | test | out-of-order injected line for GH-19 verification
audit-decisions: FAIL (1 unlogged/inconsistent claim(s)) — log them or retract the claims.
$ echo 'EXIT: 1'
```
Injected line reverted immediately after; `git diff docs/harness/DECISIONS.log` clean.

## GC sign-off

T2: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-12 | GC passed | janus | GH-19`
