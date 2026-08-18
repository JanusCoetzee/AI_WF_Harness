# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | ADR-013 — version-tagged, content-baked container images (follow-on to #31, parent #8 paused) |
| Risk tier | T2 |
| Current stage | ADR-013 ACCEPTED (ratified in-session, 2026-08-19), **not yet built** — Dockerfile `CONTENT_MODE` arg, GHCR publish workflow, OCI labels, `templates/RETRO.md`/`harness-retro` SKILL.md edits, and `THREAT-MODEL.md`'s new registry boundary row are all still-open implementation work |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session; DECISIONS.log) — ADR-013 doesn't have its own gate yet, it's a design decision awaiting a build slice |
| Next gate | None started on ADR-013's implementation. Whoever picks it up: scope as a `CHANGE.md`/ticket (touches `Dockerfile`, new CI workflow, two templates/skills, `THREAT-MODEL.md`) — the escalation trigger ADR-013 itself names (new registry boundary) means `THREAT-MODEL.md`'s delta row is written before or alongside build, not after |
| Active milestone | None active. ADR-013 decided; #31 remains fully closed out (GitHub issue #31 CLOSED); #8 remains the deliberately-paused parent |
| Current task | None — holding for direction: build ADR-013, or move to something else |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#31` shipped end to end** (built, GC-ratified, pushed, GitHub issue closed) — the container serves both browser + MCP live, `--read-only`, non-root. README's "Try it: run the container yourself" documents the dev-team pilot, deliberately scoped to localhost-only (Driver clarified the real intent wasn't production/G7 — a one-person-per-instance localhost run doesn't need real SSO, that reasoning is logged in `DECISIONS.log`). `pilot-feedback` GitHub label created for triaging what comes back.
- **`ADR-013` accepted (ratified in-session, 2026-08-19), not yet built.** Decision: publish version-tagged, content-baked images to GHCR (`CONTENT_MODE` build arg, one `Dockerfile`, mount-mode kept unchanged for adopting teams) — solves the pilot's onboarding friction (`pull && run`) and answers the still-open AWS content-sourcing question (2026-08-18 discussion) with one reusable mechanism instead of two decided separately. Driver's explicit ask (retro captures container/skills metadata) is designed, not just gestured at: OCI labels at build time, a new `templates/RETRO.md` sweep table, a new `harness-retro` SKILL.md step. **Real follow-on work still owed, named up front in the ADR itself**: `THREAT-MODEL.md` needs a new boundary row for the registry (escalation trigger tripped — that's why this went through an ADR, not a fast-path `CHANGE.md`) before/alongside the actual build.
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
