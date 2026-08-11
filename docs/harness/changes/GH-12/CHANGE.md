# CHANGE — GH-12 gate-check.sh: G3/G5/G6/G7 must resolve per-work-item evidence

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #12 — surfaced in an ad-hoc audit, 2026-08-11 |
| Date | 2026-08-11 |
| Risk tier | T2 — internal governance tooling; no customer data, no external interface |
| Recon | required (light — see RECON.md) |
| Linked records | none checked pre-existing; this change itself documents a false-PASS defect in the harness's own gate mechanics |
| Timing constraints | none — local tool, no freeze windows |
| Constitution sections consulted | §2 (verify loop — standards are failing conditions, not review feedback), §5 (traceability — gate evidence must actually attest the work item under review), §8 (brownfield — understand before changing, cite file:line) |

## Intent

`gate-check.sh` G0/G1/G2/GC resolve evidence under `docs/harness/changes/<id>/`
when given a work-item id; G3/G5/G6/G7 never got that treatment and still read a
flat `docs/harness/` path. Done means all eight gate cases accept the same
optional id and G5/G6/G7 stop reporting stale, unrelated evidence as a PASS.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-12.1 | Given no id arg, when G3/G5/G6/G7 run, then behavior is unchanged (flat `docs/harness/` path — back-compat for repos not using per-item dirs) |
| GH-12.2 | Given an id arg (e.g. `G5 GH-8`), when no `docs/harness/changes/GH-8/review-record.md` exists, then gate-check reports it missing (not the flat file) |
| GH-12.3 | Characterization: the current false-PASS is pinned as a test/fixture *before* the fix, showing `G5`/`G6`/`G7` with no id arg still exercise the pre-existing flat-path fallback deliberately, not silently |

## Regulated / reported outputs

N/A — internal tooling; nothing here feeds a regulator, tax, or financial report.

## Remediation of past impact

The defect means any G5/G6/G7 `gate-check.sh` run against work items #8/#9/#10
so far would have reported a false PASS if invoked without an id. Checked
`DECISIONS.log`: no G5/G6/G7 passage has actually been logged for #8/#9/#10 —
the false signal was never acted on. Disposition: forward-only fix, no
retroactive gate re-opening needed. Recorded here per §8's "understand before
changing" — the gap was live but never exploited.

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/gate-check.sh` only |
| Known consumers of touched behavior | humans running gate checks by hand; not called from CI (`verify.yml` doesn't invoke it) |
| Data elements involved + classification | none — reads local markdown evidence files, Internal at most |
| Deploy surface | script only, no build/deploy step |

## Rollback note

Revert the commit. No migration, no config, no consumer that adapts programmatically.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — extends the exact `evidence_dir(id)` pattern G0-G2 already use | ADR |
| Effort beyond ~3 days after recon? | No — under an hour | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T2: Driver. `DECISIONS.log`: `2026-08-11 | GC passed | janus | GH-12`
