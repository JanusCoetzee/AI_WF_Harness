# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 05-review next — #8 (M0+M1+M2) built end to end; #11 needs G5+G6 |
| Last gate passed | G4 for #11, 2026-08-18 (in-session Driver approval; DECISIONS.log) |
| Next gate | G5 for #11 (adversarial self-review, same ADR-011 override shape as #10's — would be use #3 of 3, the tripwire itself) |
| Active milestone | M2 complete (build + G4). #8 as a whole: built, not yet fully reviewed/secured (#11 G5/G6 outstanding), not deployed (G7 not applicable — no real ECS target yet) |
| Current task | None — holding for direction: G5 for #11, or pause #8 here |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) complete: build + G4 + G5 + G6 all passed.** Along the way: a CI break (gitleaks false-positived on G5's own review-record.md prose) diagnosed and fixed forward, not by rewriting pushed history. G6's threat-model delta (appended to `docs/harness/changes/GH-8/THREAT-MODEL.md`) verified the flagship prompt-injection mitigation and RBAC-at-retrieval *live*, and restated real-SSO as a **G7 deployment blocker** — `#10` ships a stub identity header only, by design.
- **`#11` built and G4-passed.** `app/mcp_server.py`: `MCPServer`, `streamable-http` only, `StubTokenVerifier` mirroring `#10`'s header stub, four ADR-002 tools, wired to `#10`'s existing `is_allowed()`/content-store directly. All 5 ACs verified **live over the real MCP JSON-RPC protocol**: unauthenticated request got a 401 at the transport layer itself (SDK-enforced); authenticated `initialize`→`tools/list`→`tools/call` returned real content with correct provenance. `verify.sh` ALL GREEN (73 tests, 94% cov). `#8` (M0+M1+M2) is now built end to end.
- **⚠️ ADR-011 tripwire: `#11`'s G5, if self-reviewed under the override, is use #3 of 3 — the trigger itself fires.** Per ADR-011's own terms, that ends the bootstrap exception on the spot: no more self-reviewed G5s in this repo after it, until a second reviewer is found. Worth deciding *before* running `#11`'s G5, not discovering it mid-review: either find real independent review for `#11` now, or knowingly spend the last use and be done with self-review as an option going forward.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed; sharper landmine found in `#10`'s G5 — bare `#NN` doesn't match its ID regex at all). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open. `#9`'s own G6/threat-model delta was also never done — named in `THREAT-MODEL.md`, not backfilled.
