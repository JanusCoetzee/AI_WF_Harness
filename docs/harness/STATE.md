# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 07-release next — #11 (and #8 as a whole: M0+M1+M2) built, reviewed, and secured. G7 not started, and already known-blocked |
| Last gate passed | G6 for #11, 2026-08-18 (Driver verdict "Approve" via issue #11 comment, ADR-012; DECISIONS.log) |
| Next gate | G7 for #8 (real deploy) — **known-blocked**: both #10's and #11's threat-model deltas name Assumption #1 (real SSO/OIDC) as an explicit G7 deployment blocker, unresolved by either slice. G7 needs that solved first, not just a checklist walk |
| Active milestone | M0+M1+M2 all complete: build + G4 + G5 + G6 passed for both #10 and #11. #8 is fully built, reviewed, and secured — only real deploy remains, and it's gated on real SSO existing |
| Current task | None — holding for direction: tackle real SSO/OIDC as its own work item (unblocks G7), or pause #8 here since M0-M2 is a legitimate, demoable stopping point |
| Blockers | none for #8/#9/#10/#11's pipeline. **ADR-011's self-review bootstrap override is now CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, no more self-review, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#8` is fully built, reviewed, and secured: M0+M1+M2, build + G4 + G5 + G6 all passed for both `#10` and `#11`.** `#11`'s G6: secret scan clean, dep audit clean (`mcp==2.0.0` + transitive), threat-model delta closes the two rows `#10`'s delta left `N/A` (excessive agency, query-leak — both mechanically tested), one new item named for future audit cycles (`mcp==2.0.0`'s OAuth middleware is a supply-chain trust dependency this repo doesn't own). AI-feature checks were the first in this repo actually load-bearing rather than N/A — all PASS. Driver verdict "Approved" via issue #11 comment, confirmed by timestamp against the earlier G5 "Approved" before logging (ADR-012 discipline).
- **ADR-012 held up twice in the same session it was written** (G5's `Approve`, G6's `Approve`) — both times the actual comment was fetched and read before anything was logged, never inferred from chat. Worth treating as validated, not just proposed.
- **⚠️ Two things now block real progress, both need a Driver decision, neither is a checklist item:** (1) ADR-011's self-review bootstrap override is **CLOSED** (trigger #4 fired on `#11`'s G5) — any future T2/T3 G5 in this repo needs a real second reviewer, no more self-review, until one is found or ADR-011 is superseded. (2) **G7 for `#8` is known-blocked on real SSO/OIDC** — both `#10`'s and `#11`'s threat-model deltas flagged this, unresolved by either. Carried forward, unchanged: `.venv/bin/pip-audit`'s stale shebang (repo housekeeping); `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs (not yet filed); GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
