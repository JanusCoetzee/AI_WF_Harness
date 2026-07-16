# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | CHG-001 — /api/health endpoint + UI document counts (harness browser) |
| Risk tier | T2 |
| Current stage | 04-implementation (complete) |
| Last gate passed | GC (2026-07-17, DECISIONS.log) |
| Next gate | G4 — evidence: verify log ✓, demo record ✓ |
| Active milestone | — (fast path: single slice, built) |
| Current task | G4 passage |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- E2E drill of the brownfield fast path started (gate approvals SIMULATED, marked).
- Next: CHANGE.md intake for CHG-001.
- Flask server on :5050 is running pre-change code; restart is the deploy step.
