# CHANGE — CHG-001 Health endpoint and document counts for the harness browser

One page, no more. If this document wants to grow, that's an escalation trigger, not
a formatting problem.

| Field | Value |
| --- | --- |
| Status | Draft |
| Driver | janus |
| Source (ticket / requester — named) | janus — "run a full end-to-end test of the harness on a sample change" (no tracker for this repo; CHG-001 allocated) |
| Date | 2026-07-17 |
| Risk tier | T2 — internal tooling, localhost-bound, no customer data, no money movement; not T3 because it ships into the committed harness that other repos copy |
| Recon | required |

## Intent

Operators of the harness browser have no machine-checkable way to confirm the app is
up and serving the full catalog. Done means a `/api/health` endpoint reports status
plus document/skill counts, and the home page shows the same counts to humans.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| CHG-001.1 | Given the server is running, when GET /api/health is called, then it returns 200 with JSON containing status "ok", a documents count, and a skills count |
| CHG-001.2 | Given the home page is rendered, when the hero section loads, then it displays the same documents and skills counts as /api/health |
| CHG-001.3 | Given any existing route (/, /s/..., /api/catalog), when called after the change, then behavior is unchanged (pinned by characterization tests) |

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | app/server.py (one new route), app/templates/index.html (hero line) |
| Known consumers of touched behavior | humans in a browser; no known programmatic consumers of /api/catalog yet |
| Data elements involved + classification | document titles/counts already public within the repo — Internal |
| Deploy surface (config, migration, infra?) | code only; deploy = restart the local server process |

## Rollback note

Revert the commit — no migration, no config change, no consumer adapts (the new
endpoint has no consumers until announced; UI counts are cosmetic).

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — extends the existing read-only localhost catalog API within the same trust boundary; exposes only counts already derivable from /api/catalog | G2 (threat model + ADR) |
| Decision that deviates from the existing pattern in this codebase? | No — same Flask route + Jinja pattern as existing code | ADR required before build |
| Effort beyond ~3 days after recon? | No — hours | G1 (full PRD) |
| Tier raised during recon? | No | Re-approve intake at new tier |

## GC sign-off

T2: Driver. Record in `DECISIONS.log`.
