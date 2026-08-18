# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 04-implementation next — #11 (M2) ticketed and task-decomposed, ready to build |
| Last gate passed | G6 for #10, 2026-08-18 (in-session Driver approval; secure-gate-record.md at docs/harness/changes/GH-10/; DECISIONS.log) |
| Next gate | G4 for #11 (build + verify), once M2's tasks (T2.1-T2.4) are done |
| Active milestone | M2 — #11 MCP tools (docs/harness/PLAN.md; transport hedge resolved to HTTP-only, Driver-confirmed 2026-08-18; skills[] confirmed out of scope) |
| Current task | Starting #11's build: app/mcp_server.py (streamable-http, imports app/doctrine.py directly), stub TokenVerifier, four ADR-002 tools, tests/test_mcp_doctrine.py |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) complete: build + G4 + G5 + G6 all passed.** Along the way: a CI break (gitleaks false-positived on G5's own review-record.md prose) diagnosed and fixed forward, not by rewriting pushed history. G6's threat-model delta (appended to `docs/harness/changes/GH-8/THREAT-MODEL.md`) verified the flagship prompt-injection mitigation and RBAC-at-retrieval *live*, and restated real-SSO as a **G7 deployment blocker** — `#10` ships a stub identity header only, by design.
- **`#11` ticketed with fresh eyes, not mechanically decomposed**: its GitHub issue had sat untouched since 2026-07-19 — predates ADR-008, never revisited unlike `#10`'s 2026-08-12 pass. Found a real CLAUDE.md §9 violation in its own text: "stdio + HTTP transport as the SDK supports" is an unresolved hedge. Checked against real MCP Python SDK docs before deciding: **stdio has no per-request identity at all** (fails ADR-002's fail-closed RBAC by construction, re-introduces the vendoring problem ADR-002 exists to prevent). Presented finding + recommendation to Driver; **confirmed HTTP-only**. Issue rewritten, `PLAN.md`'s M2 decomposed to `#10`'s task-list depth (T2.1-T2.4). Ready to build.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed; sharper landmine found in `#10`'s G5 — bare `#NN` doesn't match its ID regex at all). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open. `#9`'s own G6/threat-model delta was also never done — named in `THREAT-MODEL.md`, not backfilled.
