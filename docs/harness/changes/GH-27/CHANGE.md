# CHANGE — GH-27 templates/CHANGE.md: add a delivery-medium/consumption-context prompt

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #27 — found via real harness usage (AU_YEAR_9_MATH, CHG-001, retro 2026-08-18) |
| Date | 2026-08-18 |
| Risk tier | T3 — template prose only, no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level addition to a template's Intent section, same category as GH-15/GH-25) |
| Linked records | `docs/RETROS/RETRO-2026-08-18.md` — action #1; pairs with GH-29 (the generic CLAUDE.md §9 rule this template addition cross-references) |
| Timing constraints | none |
| Constitution sections consulted | §8 (retroactive documentation — closes exactly the gap the retro found) |

## Intent

CHG-001 (AU_YEAR_9_MATH) drafted an acceptance criterion as "markdown lints
clean, **or** HTML passes html-validate" — an unresolved hedge between two
deliverable formats — and GC ratified it without the delivery medium
(screen vs. print/physical binder) ever being asked about, causing a
post-G4 rebuild. `templates/CHANGE.md` had nowhere for that question to
surface at intake. Done means the template's Intent section prompts for
delivery medium whenever the change produces a user-facing document.

## Acceptance criteria

| # | Given / When | Then |
| --- | --- | --- |
| GH-27.1 | `templates/CHANGE.md`'s Intent section | contains an explicit prompt for delivery medium/consumption context, scoped to changes producing a user-facing document |
| GH-27.2 | The new prompt | cross-references CLAUDE.md §9's "X or Y is not an answer" rule (GH-29), naming the hedge itself as the tell |
| GH-27.3 | Every existing real `CHANGE.md` dossier in this repo | still passes `gate-check.sh GC` — a template addition must not retroactively break already-ratified dossiers |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `templates/CHANGE.md` only |
| Known consumers | every future `/harness-change` invocation; humans drafting a CHANGE.md by hand |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit — no migration, no config, no consumer that adapts
programmatically (existing dossiers don't reference this section).

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — same conditional-prompt pattern the "Regulated / reported outputs" section already uses | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. `DECISIONS.log`: `2026-08-18 | GC passed | janus | GH-27`
