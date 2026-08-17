# CHANGE — GH-29 CLAUDE.md §9: port the "X or Y is unresolved" rule upstream

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #29 — already drafted and proven in a downstream vendored copy (AU_YEAR_9_MATH), ported to canonical source per ADR-002's doctrine-flows-from-source model |
| Date | 2026-08-18 |
| Risk tier | T3 — constitution prose only, no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level addition, wording already field-tested downstream) |
| Linked records | `docs/RETROS/RETRO-2026-08-18.md` — action #4 (marked done downstream, this ticket is the upstream sync); pairs with GH-27 |
| Timing constraints | none |
| Constitution sections consulted | §8 (retroactive documentation — closing a gap already found and fixed once) |

## Intent

CHG-001's rework traced to an acceptance criterion hedging between two
outcomes ("markdown or HTML") that nobody treated as an unresolved question.
The rule fixing this was already drafted and proven in AU_YEAR_9_MATH's
vendored `CLAUDE.md` — this change ports it to the canonical source so every
future adopting repo gets it, not just the one that found it.

## Acceptance criteria

| # | Given / When | Then |
| --- | --- | --- |
| GH-29.1 | `CLAUDE.md` §9 | contains the "X or Y is an unresolved question" rule, citing `docs/RETROS/RETRO-2026-08-18.md` |
| GH-29.2 | `CLAUDE.md`'s total line count | stays under the file's own ~150-line self-imposed ceiling (was 117, is 123 after this change) |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `CLAUDE.md` §9 only |
| Known consumers | every session that reads this repo's `CLAUDE.md` — i.e. every future session |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit — no migration, no config, no consumer that adapts programmatically.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — same bullet-list format as the rest of §9 | ADR |
| Effort beyond ~3 days after recon? | No — minutes, wording already field-tested | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. `DECISIONS.log`: `2026-08-18 | GC passed | janus | GH-29`
