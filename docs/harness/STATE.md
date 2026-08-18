# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 07-release-deployment next — #10's build, G4, G5, G6 all passed; #11 (M2) not yet decomposed |
| Last gate passed | G6 for #10, 2026-08-18 (in-session Driver approval; secure-gate-record.md at docs/harness/changes/GH-10/; DECISIONS.log) |
| Next gate | G7 for #10 (release: evidence bundle, rollback rehearsal, progressive rollout) — **not applicable yet**: #10 is a library-level API slice with no deploy target of its own (ADR-002's ECS deploy is real infra, out of scope until #11/MCP lands and there's something worth standing up). Realistic next: decompose #11 (M2) to task level |
| Active milestone | M1 complete (build + G4 + G5 + G6). M2 — #11 MCP tools not yet decomposed to task level |
| Current task | None — holding for direction: decompose #11, or discuss G7/deploy timing for #8 as a whole |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) complete: build + G4 + G5 + G6 all passed.** Along the way: a CI break (gitleaks false-positived on G5's own review-record.md prose) diagnosed and fixed forward, not by rewriting pushed history — one disclosed residual on a full-history rescan, confirmed non-secret, logged. G6's threat-model delta (appended to `docs/harness/changes/GH-8/THREAT-MODEL.md`) verified the flagship prompt-injection mitigation and RBAC-at-retrieval *live*, and restated real-SSO as a **G7 deployment blocker** — `#10` ships a stub identity header only, by design. Also named, not backfilled: `#9`'s own G6/threat-model delta was never done.
- **Next choice**: decompose `#11` (MCP tools, M2) to task level — `PLAN.md` says do this once `#10` is G4-complete, which it now is (G5/G6 too). `#10`'s own G7 isn't applicable yet (no deploy target until `#11` lands and there's something worth standing up on ECS) — that's a separate conversation from `#11`'s build.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed; sharper landmine found in `#10`'s G5 — bare `#NN` doesn't match its ID regex at all). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open.
