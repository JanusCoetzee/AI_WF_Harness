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

- #9 shipped+proven (docker --read-only, healthy, pip-audit clean); Driver packaging/testing the container independently; G5 review of #9 open.
- Next: #10 doctrine API+authz (blocks #11 MCP); Driver may author blind ground truth in evals/harness/ground-truth/ first — check before building.
- Landmine: no "latest" doctrine endpoint ever (ADR-002); RBAC lives at the retrieval boundary, never in-model (ADR-002 amendment).
