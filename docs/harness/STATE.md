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
| Current task | `#33` built, GC not yet requested. **Now building `#35`** (Driver: "#33 then #35") — `templates/ISSUE.md`'s lightweight mid-build collapse path |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#32` built** (Dockerfile multi-stage, two real defects found+fixed live, `.github/workflows/publish-image.yml` written, `THREAT-MODEL.md` delta written), **GC not yet requested. Real `v*` tag push explicitly declined by the Driver** — an actual no, not deferred.
- **`#33` built.** `templates/RETRO.md` gained the "Pilot container/skills metadata sweep" table (same shape as `ADR-006`'s drift sweep); `harness-retro`'s `SKILL.md` gained step 5 (sweep `pilot-feedback` issues against the current tag, flag stale ones for triage); `README.md`'s ask gained the metadata-inclusion line. Sweep mechanics verified via a synthetic (clearly labeled, not filed for real) `pilot-feedback` report — correctly flagged as stale against `harness.config.yaml`'s current pin. GC not yet requested.
- **`ADR-014` ratified, `#35` opened as its first self-application** (still not started — building it now per "`#33` then `#35`"): `templates/ISSUE.md` needs a lightweight collapse path for tickets filed mid-build, reusing `ADR-010`'s already-decided one-file/case-conditional pattern. Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
