# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 03→04 handoff (build slices ticketed: #9 container, #10 doctrine API+authz, #11 MCP) |
| Last gate passed | G2 (2026-07-19, ADR-002 Option C ratified, DECISIONS.log) |
| Next gate | G4 — first build slice is #9 (independently shippable) |
| Active milestone | #9 containerized browser (~half day, proof: docker run + /api/health) |
| Current task | start #9 on Driver's go |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- #8 opened; ADR-002 (3 options, C recommended) + T2 threat model drafted; G2 awaits Driver.
- After G2: ticket build slices (containerize browser; MCP endpoint) via /harness-issues.
- Landmine: no "latest" doctrine endpoint ever — version pin is a contract (ADR-002).
