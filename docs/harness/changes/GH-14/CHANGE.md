# CHANGE — GH-14 Sanitize rendered markdown in the harness browser

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #14 — surfaced in an ad-hoc audit, 2026-08-11 |
| Date | 2026-08-12 |
| Risk tier | T2 — internal tooling today, but this render path is the one ADR-002/ADR-008 point at a shared, multi-BU service; no customer data, no money movement |
| Recon | required — done, see RECON.md |
| Linked records | GH-14 (this is its own fix, not remediating a separate audit finding) |
| Timing constraints | none |
| Constitution sections consulted | §3 (don't hand-roll a security boundary when a vetted library exists — informed ADR-009's Option A/B call), §6 (data handling — N/A here, no secrets/PII involved, still cited because this is a security-relevant boundary), §8 (recon before changing; RECON.md confirms no current doc depends on the behavior being removed) |

## Intent

`app/templates/page.html:10` renders markdown output via `{{ body | safe }}`,
and python-markdown passes raw HTML in `.md` sources through unchanged — a
stored-XSS surface (ADR-009 has the full analysis). Done means rendered HTML
is sanitized against an allowlist that still covers every construct the repo's
docs actually use (tables, code, lists, links, headings), with a test pinning
that a `<script>`-bearing markdown source can no longer produce a live
`<script>` tag in the response.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- | --- |
| GH-14.1 | Given a markdown source containing `<script>alert(1)</script>`, when rendered via `page()`, then the response contains no executable `<script>` tag |
| GH-14.2 | Given every existing doc under docs/stages/gates/templates/.claude/skills, when rendered, then output is unchanged for legitimate constructs (tables, code blocks, lists, links, headings) — all 21 pre-existing tests stay green |
| GH-14.3 | `bleach` pinned in app/requirements.txt, checked clean by `pip-audit` before landing |

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | app/server.py `page()` only; new dependency `app/requirements.txt` |
| Known consumers of touched behavior | `/s/<section>/<slug>` route; all browser page views |
| Data elements involved + classification | none — repo documents already Internal at most |
| Deploy surface | Dockerfile rebuild picks up the new dependency automatically (no Dockerfile change needed — `pip install -r requirements.txt` already runs at build) |

## Rollback note

Revert the commit; `bleach` drops out of the next image build. No migration,
no config, no consumer that adapts (sanitization is transparent to legitimate
content per RECON's allowlist coverage check).

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same route, hardening the existing render path | G2 |
| Decision that deviates from the existing pattern in this codebase? | **Yes** — introduces a sanitization boundary and a new dependency for a security-relevant decision | ADR required before build — **ADR-009 written and accepted** |
| Effort beyond ~3 days after recon? | No — well under a day | G1 |
| Tier raised during recon? | No | re-approve |

Per the "yes" above: ADR-009 (Sanitize rendered markdown HTML) is written and
accepted before implementation, satisfying the trigger without a full G2 —
GH-14's blast radius is one file, not a new architecture.

## GC sign-off

T2: Driver. `DECISIONS.log`: `2026-08-12 | GC passed | janus | GH-14`
