# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 06-security-compliance next — #11's G5 passed, G6 (secure-gate-record) not started |
| Last gate passed | G5 for #11, 2026-08-18 (Driver verdict "Approve" via issue #11 comment, ADR-012; DECISIONS.log) |
| Next gate | G6 for #11 (secure-gate-record: secret scan, dep audit, threat-model delta, data sweep) |
| Active milestone | M2 build + G4 + G5 complete. #8 as a whole: built + reviewed, G6 for #11 and real deploy (G7) still ahead |
| Current task | None — holding for direction: G6 for #11 |
| Blockers | none for #8/#9/#10/#11's pipeline. **ADR-011's self-review bootstrap override is now CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, no more self-review, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#11` built, G4-passed, and now G5-passed** (`app/mcp_server.py`: `MCPServer`, `streamable-http` only, four ADR-002 tools wired to `#10`'s `is_allowed()`/content-store directly; all 5 ACs verified live over the real MCP JSON-RPC protocol; `verify.sh` ALL GREEN, 73 tests, 94% cov). `#8` (M0+M1+M2) is now built end to end and reviewed. Next gate: G6 for `#11`.
- **ADR-012 landed and proved itself in the same session it was written.** The Driver named "review overload" after GH-17-21/24-29 + #10/#11's build+gate cycles piled up silently; ADR-012 routes gate/ADR/override verdicts through a GitHub issue comment instead of chat. First use: `#11`'s G5 verdict was requested as a comment on issue #11, the Driver replied `Approved` there, the comment was actually fetched and read (`gh issue view 11 --json comments`) before logging it — not inferred from this chat.
- **⚠️ ADR-011's bootstrap override is now CLOSED — trigger #4 fired.** `#11`'s G5 was use #3 of 3 (after `#9`, `#10`) with no external review ever occurring. Addendum appended to `ADR-011` itself. **No future T2/T3 G5 in this repo may self-review** until a real second reviewer is found (trigger #1) or ADR-011 is explicitly superseded — this is the load-bearing landmine for whoever runs `#11`'s eventual successor or any other T2/T3 work needing G5 next. Carried forward, unchanged: `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs (not yet filed); GH-22's RR-05 template gap still open.
