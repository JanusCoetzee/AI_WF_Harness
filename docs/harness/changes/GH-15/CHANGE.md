# CHANGE — GH-15 README directory map / quickstart drift

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #15 — surfaced in an ad-hoc audit, 2026-08-11 |
| Date | 2026-08-12 |
| Risk tier | T3 — documentation only, no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level: README additions describing files that already exist and are already load-bearing) |
| Linked records | none |
| Timing constraints | none |
| Constitution sections consulted | §8 (retroactive documentation only for what's touched — this closes exactly the gap the audit found, no wider archaeology) |

## Intent

README's directory map and Quickstart don't mention `docs/harness/OPERATING-PROTOCOL.md` (which CLAUDE.md now delegates all mechanics to, per the in-flight ADR-003 split) or the three newer scripts (`data-scan.sh`, `req-trace.sh`, `audit-decisions.sh`) already wired into the verify loop. Done means both are visible in the map and Quickstart step 1 tells an adopter to copy `OPERATING-PROTOCOL.md` along with `CLAUDE.md`.

## Acceptance criteria

| # | Given / When | Then |
| --- | --- | --- |
| GH-15.1 | Directory map's `docs/` block | lists `docs/harness/OPERATING-PROTOCOL.md` alongside `PHILOSOPHY.md`/`OPERATING-MODEL.md` |
| GH-15.2 | Directory map's `scripts/` block | lists `data-scan.sh`, `req-trace.sh`, `audit-decisions.sh` |
| GH-15.3 | Quickstart step 1 | includes `docs/harness/OPERATING-PROTOCOL.md` in the copy list |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | README.md only |
| Known consumers | humans reading README when adopting the harness |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — describes files already present, no new convention | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. `DECISIONS.log`: `2026-08-12 | GC passed | janus | GH-15`
