# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #31 — containerize #11's MCP process alongside #9's browser (parent: #8, paused) |
| Risk tier | T2 |
| Current stage | **#31 RATIFIED (GC) and complete** — built, all 7 ACs verified live, GC approved in-session 2026-08-18. No further gate owed at this size (small fast-path item, build evidence doubled as G4-equivalent proof, same as GH-17..21) |
| Last gate passed | GC for #31, 2026-08-18 (Driver "Approve" rendered in-session — checked issue #31 first, confirmed no comment existed yet, not inferred; noted on the issue for the record; DECISIONS.log) |
| Next gate | None owed on #31 — done. Parent #8 stays paused (Driver's Option-1 decision, unchanged); if resumed directly (shared/production), G7 starts at real SSO/OIDC |
| Active milestone | None active. #31's work is done (GitHub issue itself left open, not closed — that's a separate human action); #8 remains the deliberately-paused parent |
| Current task | None — holding for next direction |
| Blockers | none blocking #31. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#31` RATIFIED (GC) and done** (`#8` stays deliberately paused, unchanged — `#31` was standalone). `Dockerfile` now installs `git`, launches both `gunicorn` and `app/mcp_server.py` via `scripts/container-entrypoint.sh` (independent foreground children, one dying doesn't kill the other), `scripts/container-healthcheck.py` checks both and names which failed. **Real defect found and fixed forward**, not `#31`-specific: `python:3.12-slim` never had `git`, but `_git_commit()` needs it for every manifest — `#10`'s own already-shipped, already-G4/G5/G6-passed route would have failed identically in the real container, just never exercised there. All 7 ACs verified live (`docker build && docker run --read-only`). AC #6 narrowed from the original ticket per a real Docker-HEALTHCHECK-is-one-bit constraint found in recon — named, not silently reinterpreted. Driver approved in-session (not via the issue #31 comment ADR-012 defaults to) — checked the issue first, confirmed nothing was posted there yet before logging, then noted it on the issue anyway so the ticket stays a complete record.
- **README updated for dev-team pilot use, distinct from a production/G7 decision.** Driver clarified `#31`'s real purpose: not shipping a product, exposing the container to the dev team for feedback — asked, not assumed, which exposure surface (localhost-only per dev, chosen over shared-network or internet-reachable). That materially changes the risk picture: `THREAT-MODEL.md` Assumption #1 (real SSO) was written for a shared, network-reachable service — a one-person-per-instance localhost run has nobody else on that trust boundary, so stub auth adds no incremental exposure. Documented explicitly in README's new "Try it: run the container yourself" section, logged as a real decision in `DECISIONS.log`, new `pilot-feedback` GitHub label created. **Does not touch or relax the SSO blocker for any shared/production deploy.**
- Carried forward, unchanged: **ADR-011's self-review bootstrap override is CLOSED**; if `#8` is picked back up directly (shared/production), G7 still starts at real SSO/OIDC. `.venv/bin/pip-audit`'s stale shebang; `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs; GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
