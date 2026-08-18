# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #32 — publish version-tagged, content-baked images to GHCR (ADR-013, parent #8 paused) |
| Risk tier | T2 |
| Current stage | #32 **built and live-verified locally**, GC verdict not yet requested. **Real GHCR publish explicitly declined by the Driver for now** ("I do not want to create a public image yet") — not a pending question, an actual no |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session; DECISIONS.log) |
| Next gate | GC for #32 — `docs/harness/changes/GH-32/CHANGE.md`+`RECON.md` ready, live proof recorded (both build modes, all local ACs). `gate-check.sh GC GH-32` mechanically FAILs on the escalation trigger, expected and correct (satisfied by `ADR-013` already accepted pre-build, same shape as GH-14/ADR-009) — not a defect to fix |
| Active milestone | #32 (standalone, off paused #8). Build complete for GH-32.1-3/.5; GH-32.4 (real publish) held pending explicit go-ahead |
| Current task | None in progress. **#35 (open, ready)** — `templates/ISSUE.md` needs a lightweight mid-build collapse path (`ADR-014`'s own new obligation, applied to itself: ticket filed before any template edit). Holding for direction: build #35, or Driver's GC verdict on #32 first |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#32` built, all local ACs live-verified, GC not yet requested.** `Dockerfile` is multi-stage (`base`/`mount`/`baked`/`final`, `CONTENT_MODE` arg, mount-mode confirmed byte-identical). Two real defects found live and fixed: `harness.config.yaml` also needed in `HARNESS_ROOT` for baked mode; git's "dubious ownership" check needed `git config --system --add safe.directory /harness` (fixed for both modes — mount mode only avoided it by bind-mount luck, not a guarantee). `.github/workflows/publish-image.yml` written and YAML-validated; `THREAT-MODEL.md`'s new registry-boundary row written. **Real `v*` tag push explicitly declined by the Driver** ("I do not want to create a public image yet") — an actual no, not deferred. `#33` still not started.
- **`ADR-014` ratified (2026-08-19), and `#35` opened as its first self-application.** `CLAUDE.md` §5: "a ticket precedes the work, not the other way round" — features/significant platform-level bugs/discrete tasks need a ticket *before* work starts even mid-build; routine in-service corrections don't need one at all (calibration anchor in the ADR: `#32`'s `harness.config.yaml` fix vs. its `git config --system` fix, the latter should have preceded `#34`, not followed it). Driver then asked whether a ticket covers what it needs to function as a real "discrete prompt" — mostly yes, but `ADR-014` itself exposed a gap: no lightweight path for a ticket filed mid-build, the full `ISSUE.md` shape is disproportionate ceremony for a fast finding. `#35` fixes that (reusing `ADR-010`'s already-decided pattern: one file, case-conditional inline collapse, not a second file) — filed before any template edit, per the very rule it implements. Not started yet.
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
