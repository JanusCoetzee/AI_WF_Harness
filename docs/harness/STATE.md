# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 02-architecture (entered at G2 via fast-path escalation: new external interface) |
| Last gate passed | — (none yet for #8; prior item CHG-001 closed at G7 2026-07-17) |
| Next gate | G2 — needs: Driver ratifies ADR-002 option choice + threat model |
| Active milestone | design slice (#8); build slices ticketed only after G2 |
| Current task | ADR-002 + threat model drafted; awaiting G2 ratification |
| Blockers | G2 is human-only |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- #8 opened; ADR-002 (3 options, C recommended) + T2 threat model drafted; G2 awaits Driver.
- After G2: ticket build slices (containerize browser; MCP endpoint) via /harness-issues.
- Landmine: no "latest" doctrine endpoint ever — version pin is a contract (ADR-002).
