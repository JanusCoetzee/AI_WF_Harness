# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #32 — publish version-tagged, content-baked images to GHCR (ADR-013, parent #8 paused) |
| Risk tier | T2 |
| Current stage | #32 **built and live-verified locally**, GC verdict not yet requested. **Real GHCR publish deliberately not exercised** — a real `v*` tag push is a public, outward-facing action needing explicit Driver confirmation first, separate from the GC verdict itself |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session; DECISIONS.log) |
| Next gate | GC for #32 — `docs/harness/changes/GH-32/CHANGE.md`+`RECON.md` ready, live proof recorded (both build modes, all local ACs). `gate-check.sh GC GH-32` mechanically FAILs on the escalation trigger, expected and correct (satisfied by `ADR-013` already accepted pre-build, same shape as GH-14/ADR-009) — not a defect to fix |
| Active milestone | #32 (standalone, off paused #8). Build complete for GH-32.1-3/.5; GH-32.4 (real publish) held pending explicit go-ahead |
| Current task | None — holding for: (1) Driver's GC verdict on #32, (2) separately, explicit confirmation before pushing a real `v*` tag (first real GHCR publish under the Driver's account) |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#32` built, all local ACs live-verified, GC not yet requested.** `Dockerfile` is now multi-stage (`base`/`mount`/`baked`/`final`, `CONTENT_MODE` arg, mount-mode confirmed byte-identical). Two real defects found live, not asserted away: (1) `build_manifest()` also needs `harness.config.yaml` from `HARNESS_ROOT` — missed on the first baked-mode attempt, 500'd, fixed; (2) git's "dubious ownership" check rejects `git rev-parse` on root-owned `COPY`'d content read by the non-root `harness` user — fixed with `git config --system --add safe.directory /harness`, applies to **both** modes since mount-mode only avoided this by bind-mount-ownership luck, not a real guarantee. `.github/workflows/publish-image.yml` written and YAML-validated (GHCR, never `:latest`, no new secret needed — repo confirmed public). `THREAT-MODEL.md`'s new registry-boundary row written, reusing ADR-008's mitigations. **Not done: a real tag push** — that's the one outward-facing action here (publishes a real public GHCR package under the Driver's account) and needs explicit confirmation, separate from the GC verdict itself.
- **`#33`** (retro captures container/skills metadata) still not started — soft-dependent on `#32`, buildable either order.
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
