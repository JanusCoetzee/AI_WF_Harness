# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #31 — containerize #11's MCP process alongside #9's browser (parent: #8, paused) |
| Risk tier | T2 |
| Current stage | B0/B1 fast path — #31 built, all 7 ACs verified live (`docker build && docker run --read-only`), GC verdict requested via issue #31 (ADR-012), pending Driver reply |
| Last gate passed | G6 for #11, 2026-08-18 (Driver verdict "Approve" via issue #11 comment, ADR-012; DECISIONS.log) — #31 hasn't reached GC yet, evidence is ready |
| Next gate | GC for #31 — `docs/harness/changes/GH-31/CHANGE.md`+`RECON.md` ready, `gate-check.sh GC GH-31` evidence PRESENT, live proof (not assertion) recorded in CHANGE.md. Verdict requested as an issue #31 comment (ADR-012), reply `Approve`/`Decline` there |
| Active milestone | #31 (standalone, off paused #8). Build complete, live-verified, GC verdict pending |
| Current task | None — holding for Driver's reply on issue #31 (Approve/Decline #31's GC) |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#31` built and live-verified, GC verdict requested** (`#8` stays deliberately paused, unchanged — `#31` is standalone). `Dockerfile` now installs `git`, launches both `gunicorn` and `app/mcp_server.py` via `scripts/container-entrypoint.sh` (independent foreground children, one dying doesn't kill the other), `scripts/container-healthcheck.py` checks both and names which failed. **Real defect found and fixed forward**, not `#31`-specific: `python:3.12-slim` never had `git`, but `_git_commit()` needs it for every manifest — `#10`'s own already-shipped, already-G4/G5/G6-passed route would have failed identically in the real container, just never exercised there (both `#10`'s and `#11`'s gate evidence ran against bare local processes, never Docker). All 7 ACs verified live (`docker build && docker run --read-only`). AC #6 narrowed from the original ticket per a real Docker-HEALTHCHECK-is-one-bit constraint found in recon — named, not silently reinterpreted. `gate-check.sh GC GH-31` evidence PRESENT. Verdict requested as an issue #31 comment (ADR-012), pending reply.
- **README updated for dev-team pilot use, distinct from a production/G7 decision.** Driver clarified `#31`'s real purpose: not shipping a product, exposing the container to the dev team for feedback — asked, not assumed, which exposure surface (localhost-only per dev, chosen over shared-network or internet-reachable). That materially changes the risk picture: `THREAT-MODEL.md` Assumption #1 (real SSO) was written for a shared, network-reachable service — a one-person-per-instance localhost run has nobody else on that trust boundary, so stub auth adds no incremental exposure. Documented explicitly in README's new "Try it: run the container yourself" section, logged as a real decision in `DECISIONS.log`, new `pilot-feedback` GitHub label created. **Does not touch or relax the SSO blocker for any shared/production deploy.**
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
