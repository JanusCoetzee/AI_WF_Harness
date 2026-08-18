# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 05-review — #11's G5 review-record.md drafted, adversarial self-review complete, pending Driver verdict |
| Last gate passed | G4 for #11, 2026-08-18 (in-session Driver approval; DECISIONS.log) |
| Next gate | G5 for #11 — verdict requested as a comment on GitHub issue #11 itself (ADR-012), reply `Approve`/`Decline` there. **This would be use #3 of 3 — ADR-011's trigger #4 tripwire fires the moment it's logged as passed.** No further self-reviewed G5 in this repo after that, until a real second reviewer is found |
| Active milestone | M2 build + G4 complete. G5 verdict requested via issue #11 (ADR-012), awaiting reply. #8 as a whole: built, G6 for #11 and real deploy (G7) still ahead |
| Current task | None — holding for Driver's reply on issue #11 (Approve/Decline #11's G5) |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) complete: build + G4 + G5 + G6 all passed.** Along the way: a CI break (gitleaks false-positived on G5's own review-record.md prose) diagnosed and fixed forward, not by rewriting pushed history. G6's threat-model delta (appended to `docs/harness/changes/GH-8/THREAT-MODEL.md`) verified the flagship prompt-injection mitigation and RBAC-at-retrieval *live*, and restated real-SSO as a **G7 deployment blocker** — `#10` ships a stub identity header only, by design.
- **`#11` built and G4-passed.** `app/mcp_server.py`: `MCPServer`, `streamable-http` only, `StubTokenVerifier` mirroring `#10`'s header stub, four ADR-002 tools, wired to `#10`'s existing `is_allowed()`/content-store directly. All 5 ACs verified **live over the real MCP JSON-RPC protocol**: unauthenticated request got a 401 at the transport layer itself (SDK-enforced); authenticated `initialize`→`tools/list`→`tools/call` returned real content with correct provenance. `verify.sh` ALL GREEN (73 tests, 94% cov). `#8` (M0+M1+M2) is now built end to end.
- **⚠️ ADR-011 tripwire: `#11`'s G5, if self-reviewed under the override, is use #3 of 3 — the trigger itself fires.** Per ADR-011's own terms, that ends the bootstrap exception on the spot: no more self-reviewed G5s in this repo after it, until a second reviewer is found. **ADR-012 (new, 2026-08-18):** the Driver named "review overload" after this session's accumulated approval backlog (GH-17-21/24-29, #10, #11) — gate/ADR/override verdicts not rendered live now go through a GitHub issue, answered as a comment. Applied immediately: `#11`'s G5 verdict request is posted as a comment on issue #11 itself, not chat. Next session: check issue #11 for a Driver reply before doing anything else with `#11`.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed; sharper landmine found in `#10`'s G5 — bare `#NN` doesn't match its ID regex at all). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open. `#9`'s own G6/threat-model delta was also never done — named in `THREAT-MODEL.md`, not backfilled.
