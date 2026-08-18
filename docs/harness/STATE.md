# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #32 / #33 / #35 — three built, standalone tickets off paused #8 (ADR-013/ADR-014 follow-ons) |
| Risk tier | T2 (#32); T3 (#33, #35) |
| Current stage | **#32/#33/#35 GC-passed, closed on GitHub, pushed.** Fully done except GH-32.4 (real GHCR publish), which is a **standing, phase-scoped decision, not a per-ticket "not yet"**: single-developer PoC phase, build + tag locally only |
| Last gate passed | GC for #32/#33/#35, 2026-08-19 (Driver verdict rendered in-session, ADR-012's synchronous carve-out; DECISIONS.log) |
| Next gate | None owed. `.github/workflows/publish-image.yml` stays written, YAML-validated, and unexercised — ready whenever the phase changes (a real second developer, moving past PoC), not deleted or disabled, just not triggered until then |
| Active milestone | None active — #32/#33/#35 fully closed out (issues CLOSED, commits pushed) |
| Current task | None — holding for next direction |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#32`/`#33`/`#35` fully closed out**: GC-passed (Driver "yes," in-session, together), issues CLOSED on GitHub with summarizing comments, commits pushed. `#32`: `Dockerfile` multi-stage, two real defects found+fixed live, `.github/workflows/publish-image.yml` + `THREAT-MODEL.md` delta written. `#33`: `templates/RETRO.md`'s new sweep table + `harness-retro`'s new step + `README.md`'s ask, verified via a labeled-synthetic report. `#35`: `templates/ISSUE.md`'s new mid-build shortcut + `harness-issues`'s new "Mode C," proven by rewriting `#34` for comparison.
- **Real GHCR publish is a standing phase-scoped decision, not a per-ticket "not yet."** Driver: single-developer PoC phase, local build+tag only. `publish-image.yml` stays written and ready, unexercised until the phase actually changes — don't re-ask this every time `#32`'s own AC comes up, it's settled until the Driver says otherwise.
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
