# CHANGE — GH-26 gate-check.sh need_file() false-positives on the `CHG-###` pattern in prose

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #26 — found via real harness usage (AU_YEAR_9_MATH, CHG-001, retro 2026-08-18) |
| Date | 2026-08-18 |
| Risk tier | T2 — this repo's own gate-mechanics tooling; wrong behavior here silently miscategorizes real work, but no money/data/regulatory surface |
| Recon | required (light — single function, single file) |
| Linked records | `docs/RETROS/RETRO-2026-08-18.md` — first real-usage retro since the harness was vendored into AU_YEAR_9_MATH; this is action #2 from it |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop — a check that produces false failures erodes trust in the whole gate mechanism), §8 (brownfield — recon before changing, cite file:line) |

## Intent

`need_file()`'s unfilled-template check flags any file containing the literal
substring `CHG-###` as unfilled, including legitimate prose that explains the
pattern itself (e.g. a traceability note). Reproduced directly against
`scripts/gate-check.sh:21` before touching anything. Done means prose
mentions no longer false-positive while genuinely unfilled placeholders
(title line, empty acceptance-criteria rows) still correctly fail.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-26.1 | Given a CHANGE.md with every real field filled in, and one prose sentence backtick-quoting `` `CHG-###` `` to explain the ID convention, when `need_file()` checks it, then it passes (no false positive) |
| GH-26.2 | Given a genuinely unfilled `templates/CHANGE.md` copy (title line + acceptance rows still bare `CHG-###`), when checked, then it still correctly fails |
| GH-26.3 | Given every existing real dossier in `docs/harness/changes/*/CHANGE.md`, when re-checked after the fix, then none regress that weren't already failing for an unrelated, pre-existing reason |

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/gate-check.sh`'s `need_file()` only — used by every gate (G0–G7, GC) that checks a templated doc |
| Known consumers of touched behavior | every future `/harness-*` skill invocation that runs `gate-check.sh`; humans running it by hand |
| Data elements involved + classification | none — reads local markdown files |
| Deploy surface | script only, no build/deploy step |

## Rollback note

Revert the commit. No migration, no config, no consumer that adapts
programmatically — `need_file()`'s call signature is unchanged.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — same regex-based check, just pre-filtered input | ADR |
| Effort beyond ~3 days after recon? | No — under an hour, verified live | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T2: Driver. `DECISIONS.log`: `2026-08-18 | GC passed | janus | GH-26`
