# CHANGE — GH-28 T3-light CHANGE.md: collapse FinServ-only fields at T3

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #28 — found via real harness usage (AU_YEAR_9_MATH, CHG-001, retro 2026-08-18); design resolved in ADR-010 |
| Date | 2026-08-18 |
| Risk tier | T3 — template prose only, no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level addition; design decision already made and recorded in ADR-010, not re-litigated here) |
| Linked records | `docs/RETROS/RETRO-2026-08-18.md` — action #3; `docs/harness/adr/ADR-010-t3-light-change-template.md` — the design decision this change implements |
| Timing constraints | none |
| Constitution sections consulted | §5 (every non-obvious decision gets an ADR — done, ADR-010), §8 (match existing pattern — `THREAT-MODEL.md`'s tier-conditional depth, not a new template file) |

## Intent

`templates/CHANGE.md`'s FinServ-inherited fields (Linked records, Timing
constraints, Regulated/reported outputs) produced zero value on a real T3
change — answered "none"/deleted every time, as any non-regulated-repo T3
change always will. ADR-010 resolved the design question (one template,
tier-conditional collapse — matching `THREAT-MODEL.md`'s existing precedent,
not a second template file). This change implements that decision.

## Acceptance criteria

| # | Given / When | Then |
| --- | --- | --- |
| GH-28.1 | `templates/CHANGE.md` | states the T3 collapse instruction once, near the field table, per ADR-010 Option B |
| GH-28.2 | Every existing real `CHANGE.md` dossier in this repo (not retroactively rewritten — new convention applies forward only, CLAUDE.md §8) | still passes `gate-check.sh GC` unchanged |
| GH-28.3 | The instruction | states the re-expand-on-promotion rule from ADR-010's Consequences, so a future T3→T1/T2 promotion isn't silently missed |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `templates/CHANGE.md` only |
| Known consumers | every future `/harness-change` invocation at any tier; humans drafting a CHANGE.md by hand |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit. No migration, no config; no existing dossier references
this instruction (it's new, forward-only), so no consumer adapts.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | **No** — matches `THREAT-MODEL.md`'s existing tier-conditional-depth pattern exactly; this is *why* Option B won in ADR-010, not a deviation | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. `DECISIONS.log`: `2026-08-18 | GC passed | janus | GH-28`
