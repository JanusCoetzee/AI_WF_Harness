# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 03→04 handoff (build slices ticketed: #9 container, #10 doctrine API+authz, #11 MCP) |
| Last gate passed | G4 for #9 (2026-07-19, docker proof healthy, DECISIONS.log) |
| Next gate | G5 review of #9 (human), then build #10 doctrine API |
| Active milestone | #10 doctrine API + authz interface (~1 day; blocks #11 MCP) |
| Current task | #9 done+proven; awaiting review or go on #10 |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- #9 shipped+proven (docker --read-only, healthy, pip-audit clean); Driver packaging/testing the container independently; G5 review of #9 open. Audit fixes (GH-12/13/14/15) shipped+pushed to main; post-fix regression check confirmed the harness front-half (G0-G3) still SATISFACTORY against frozen greenfield GT (evals/harness/runs/greenfield/run-3, REPORT.md).
- Next: #10 doctrine API+authz (blocks #11 MCP) — ADR-008 (2026-07-25) supersedes ADR-002's single-shared-service topology with independent per-BU instances; #10's manifest schema MUST add a `skills` array (composed core+skills bill-of-materials) before finalizing, or it'll need rework. ADR-002's API/MCP contracts, read-only invariant, and RBAC-at-retrieval mechanics still apply, just per-instance now.
- Landmine: no "latest" doctrine endpoint ever (ADR-002, still true); version/deprecation drift across BU instances is deliberately a human governance function, not harness-enforced (ADR-008) — don't build enforcement logic for it. Also: #16 open — review-g5/retro-g8 eval scenarios still have zero GT/coverage, meaning req-trace.sh (ADR-005) and the G5/G8 flows are unverified by the eval suite; not blocking #10 but don't assume G5/G8 mechanics are eval-proven when #10 gets there.
