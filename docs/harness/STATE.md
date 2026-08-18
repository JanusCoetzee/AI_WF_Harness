# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | **#8 PAUSED, deliberately, at M0+M1+M2** — build + G4 + G5 + G6 all passed for both #10 and #11; G7 (real deploy) not started, explicitly known-blocked, not being worked |
| Last gate passed | G6 for #11, 2026-08-18 (Driver verdict "Approve" via issue #11 comment, ADR-012; DECISIONS.log) |
| Next gate | G7 for #8 (real deploy) — **deliberately not next**. Driver chose (2026-08-18) to stop at M0-M2 rather than scope real SSO/OIDC as a follow-on to chase G7 now. When #8 is picked back up, G7 needs real SSO/OIDC solved first (THREAT-MODEL.md Assumption #1) — start there, not at a fresh recon |
| Active milestone | None active. M0+M1+M2 complete and is the intentional stopping point — #8 is fully built, reviewed, and secured; real deploy is future work, not in progress |
| Current task | None — #8 paused by Driver decision. Next session: pick a different work item, or resume #8 by scoping real SSO/OIDC first |
| Blockers | none blocking other work — #8 itself is deliberately paused, not stuck. **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#8` deliberately paused at M0+M1+M2** — Driver's explicit choice (Option 1 of 2 presented: stop here vs. scope real SSO/OIDC to chase G7). Not a stall: build + G4 + G5 + G6 all genuinely passed for both `#10` and `#11`, every verdict Driver-rendered (G4/G5 in-session for #10, G5/G6 for #11 via ADR-012's issue-comment channel), nothing left `UNVERIFIED`. `#8`'s doctrine service is real and demoable as-is (HTTP + MCP, fail-closed integrity, fail-closed authz, two rounds of security review) — it just isn't deployed, and isn't trying to be right now.
- **ADR-012 held up twice in the same session it was written** (G5's `Approve`, G6's `Approve`) — both times the actual comment was fetched and read before anything was logged, never inferred from chat. Worth treating as validated, not just proposed.
- **If `#8` is picked back up later, G7 starts at real SSO/OIDC** (THREAT-MODEL.md Assumption #1 — both `#10`'s and `#11`'s G6 deltas name it), not at a fresh recon. Separately, still live: **ADR-011's self-review bootstrap override is CLOSED** (trigger #4 fired on `#11`'s G5) — any future T2/T3 G5 in this repo needs a real second reviewer until one is found or ADR-011 is superseded. Carried forward, unchanged: `.venv/bin/pip-audit`'s stale shebang (repo housekeeping); `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs (not yet filed); GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
