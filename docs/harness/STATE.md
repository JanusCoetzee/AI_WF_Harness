# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | ADR-013 — version-tagged, content-baked container images (follow-on to #31, parent #8 paused) |
| Risk tier | T2 |
| Current stage | ADR-013 ACCEPTED, scoped as two tickets, **neither built yet**: #32 (publish tagged/baked images to GHCR) and #33 (harness-retro captures container/skills metadata) |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session; DECISIONS.log) |
| Next gate | None started. #32 is the one with a real unknown (registry/CI setup) and the named escalation trigger (`THREAT-MODEL.md`'s new registry boundary row, before/alongside build). #33 is pure docs/template, soft-dependent on #32, buildable in either order |
| Active milestone | None active. #31 fully shipped and closed; ADR-013 decided; #32/#33 ready (Definition of Ready met), neither started; #8 remains the deliberately-paused parent |
| Current task | None — holding for direction: build #32, build #33, or move to something else |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#31` shipped end to end** (built, GC-ratified, pushed, GitHub issue closed) — the container serves both browser + MCP live, `--read-only`, non-root. README's "Try it: run the container yourself" documents the dev-team pilot, deliberately scoped to localhost-only (Driver clarified the real intent wasn't production/G7 — a one-person-per-instance localhost run doesn't need real SSO, that reasoning is logged in `DECISIONS.log`). `pilot-feedback` GitHub label created for triaging what comes back.
- **`ADR-013` accepted (ratified in-session, 2026-08-19), scoped as `#32`+`#33`, neither built.** `#32`: publish version-tagged, content-baked images to GHCR (`CONTENT_MODE` build arg, one `Dockerfile`, mount-mode unchanged for adopting teams; OCI labels; `THREAT-MODEL.md`'s new registry boundary row, named as the escalation trigger up front, not deferred). `#33`: `templates/RETRO.md` gains a "Pilot container/skills metadata sweep" table, `harness-retro`'s `SKILL.md` gains a sweep step, `README.md`'s `pilot-feedback` ask gains the metadata-inclusion line — soft-dependent on `#32` (nothing real to sweep until images publish, but buildable independently). Split deliberately into two tickets, not one, since they have different real dependencies (registry/CI setup vs. pure docs).
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
