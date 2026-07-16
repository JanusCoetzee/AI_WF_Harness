# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | CHG-001 — /api/health endpoint + UI document counts (harness browser) |
| Risk tier | T2 |
| Current stage | 08-operate (CHG-001 released as v0.2.0) |
| Last gate passed | G7 (2026-07-17, DECISIONS.log) |
| Next gate | — (next work item starts at B0 or 00) |
| Active milestone | — |
| Current task | retro actions 1-3 (RETRO-2026-07-17.md) |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- E2E drill complete: CHG-001 through GC→G4→G5→G6→G7; all approvals SIMULATED-marked.
- Next: retro actions (strengthen G5/G6 checks, gitleaks, standards tooling).
- Server on :5050 now runs v0.2.0; /api/health is live.
