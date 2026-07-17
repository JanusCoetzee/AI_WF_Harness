# CHANGE — GH-6 Harness browser: make the eval suite browsable

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #6 — Driver, requested in-session 2026-07-17 |
| Date | 2026-07-17 |
| Risk tier | T2 — ships into the committed harness other repos copy; localhost tool, no customer data |
| Recon | required (light — single known file) |
| Linked records | none checked — no audit findings or incidents touch this |
| Timing constraints | none — local tool, no freeze windows |

## Intent

The browser doesn't catalog `evals/harness/`, so the Driver reviews the eval suite
in the repo instead of the UI. Done means an Evals section lists README, REPORT,
manifest, scenario briefs, and frozen ground truths, each rendering on its page.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-6.1 | /api/catalog contains an "evals" section listing report, manifest, gt-*, and scenario briefs |
| GH-6.2 | Every eval item page renders 200 (markdown or raw YAML) |
| GH-6.3 | All prior behavior unchanged except the deliberately moved section-keys pin |

## Regulated / reported outputs

N/A — internal documentation browser; nothing feeds a regulator, tax, or financial report.

## Remediation of past impact

N/A — no defect; feature addition.

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | app/server.py catalog() only; templates untouched (section rendering is data-driven) |
| Known consumers of touched behavior | humans in a browser; /api/catalog shape gains one section (pinned test moved deliberately) |
| Data elements involved + classification | repo documents already in the catalog's trust boundary — Internal |
| Deploy surface | code only; deploy = restart :5050 |

## Rollback note

Revert the commit + restart — no migration, no config, no consumer adapts (the new
section has no programmatic consumers).

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same localhost catalog surface, new section | G2 |
| Decision that deviates from the existing pattern? | No — same add()/_md_item pattern as every other section | ADR |
| Effort beyond ~3 days after recon? | No — under an hour | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T2: Driver. DECISIONS.log.
