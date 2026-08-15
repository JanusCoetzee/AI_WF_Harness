# CHANGE — GH-18 gate-check.sh escalation-trigger regex doesn't match bold-emphasized Yes cells

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #18 — found during GH-14, filed 2026-08-12 |
| Date | 2026-08-12 |
| Risk tier | T2 — internal governance tooling (GC gate mechanics); no customer data, no external interface |
| Recon | waived-trivial (single-line regex swap; behavior fully characterized by re-running against every existing `changes/*/CHANGE.md`, pasted below) |
| Linked records | GH-14's `CHANGE.md`/ADR-009 (the case that surfaced this — escalation was honored by policy there, but the mechanical check missed it) |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop — standards are failing conditions, not review feedback), §5 (traceability), §8 (brownfield — cite file:line) |

## Intent

`gate-check.sh`'s GC case flagged a tripped escalation trigger only for a
table cell containing exactly `Yes`/`yes` — not `**Yes**` (bold), which is
how GH-14's own `CHANGE.md` correctly answered its "deviates from the
existing pattern" trigger to make the trip visible in the rendered table.
Done means the mechanical check catches a Yes answer regardless of markdown
emphasis or trailing rationale prose in the same cell, without false-tripping
on the `| Trigger | Yes/No | If yes → |` header row.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-18.1 | Given a `CHANGE.md` answering a trigger `**Yes**` (bold, with or without trailing rationale text in the same cell), when `gate-check.sh GC <id>` runs, then it reports the escalation-tripped failure (previously: silently passed) |
| GH-18.2 | Given a `CHANGE.md` answering every trigger `No`, when `gate-check.sh GC <id>` runs, then it still reports no triggers tripped (no regression) |
| GH-18.3 | Given the literal `Yes/No` header cell present in every `CHANGE.md`'s trigger table, when `gate-check.sh GC <id>` runs, then that header cell alone does not cause a false trip |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/gate-check.sh` only (one regex in the GC case) |
| Known consumers | humans running `gate-check.sh GC` by hand; **not** wired into `scripts/verify.sh` or CI (`grep -rn gate-check scripts/verify.sh .github/workflows` — no hits), so this cannot regress CI |
| Data elements | none |
| Deploy surface | script only |

## Remediation of past impact

Re-running the fixed check against every existing change dossier: GH-14 now
correctly reports "an escalation trigger is answered 'yes'" (it was
`**Yes**`, honored by policy via ADR-009 written before build — so nothing
shipped wrong, but the mechanical check should have caught it and now does).
GH-12, GH-13, GH-15, CHG-001 all still report "no escalation triggers
tripped" (genuinely all-No, unaffected by the fix). No retroactive gate
re-opening needed — GH-14 already satisfied the trigger's actual intent
before this fix existed.

## Rollback note

Revert the commit. No migration, no consumer contract.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — same detection intent, wider match | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## Verification (manual — no test harness for this bash script)

```
$ for id in GH-12 GH-13 GH-14 GH-15 CHG-001; do
    echo "== $id =="; bash scripts/gate-check.sh GC $id 2>&1 | grep -i trigger
  done
== GH-12 ==   ✓ no escalation triggers tripped
== GH-13 ==   ✓ no escalation triggers tripped
== GH-14 ==   ✗ an escalation trigger is answered 'yes' — fast path exits to the full workflow
== GH-15 ==   ✓ no escalation triggers tripped
== CHG-001 == ✓ no escalation triggers tripped
```

## GC sign-off

T2: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-12 | GC passed | janus | GH-18`
