# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #32 / #33 / #35 — three built, standalone tickets off paused #8 (ADR-013/ADR-014 follow-ons) |
| Risk tier | T2 (#32); T3 (#33, #35) |
| Current stage | All three **built and locally verified, none has a GC verdict yet.** #32's real GHCR publish explicitly declined by the Driver for now — not pending, an actual no |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session; DECISIONS.log) |
| Next gate | GC for #32, #33, and #35 — all three have `CHANGE.md`+evidence ready, `gate-check.sh GC` passes mechanically for #33/#35; #32 mechanically FAILs on its named escalation trigger, expected (satisfied by `ADR-013` pre-build, same shape as GH-14/ADR-009) |
| Active milestone | None active — all three built, holding for Driver verdicts |
| Current task | None — holding for Driver direction: GC verdicts on #32/#33/#35, or something else |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#32`/`#33`/`#35` all built this session, none has a GC verdict yet.** `#32`: `Dockerfile` multi-stage, two real defects found+fixed live, `.github/workflows/publish-image.yml` + `THREAT-MODEL.md` delta written; real `v*` tag push explicitly declined by the Driver, an actual no. `#33`: `templates/RETRO.md`'s new "Pilot container/skills metadata sweep" table + `harness-retro`'s new sweep step + `README.md`'s metadata-inclusion ask, sweep mechanics verified via a labeled-synthetic `pilot-feedback` report. `#35`: `templates/ISSUE.md`'s new mid-build shortcut (`ADR-014`) + `harness-issues`'s new "Mode C," proven by rewriting `#34` in the new format for comparison (genuinely shorter, same substance).
- **`ADR-014` is now load-bearing on itself** — `#35` was filed under its own rule before being built, and demonstrates the rule working (a real ticket, filed first, doing real work).
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
