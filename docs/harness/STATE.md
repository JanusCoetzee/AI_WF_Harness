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
| Active milestone | #10 doctrine API + authz interface (~1 day; blocks #11 MCP) — ticket redefined 2026-08-12, scope now crystal clear |
| Current task | #9 done+proven; awaiting review. #10 ticket repaired and ready to build (see handoff) |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 redefined and ready to build**: repaired via /harness-issues Mode B, body replaced (not just commented) on GitHub. Resolved crystal-clear: `skills` array (ADR-008) IS in #10's own manifest schema — reports this instance's composition sourced from `harness.config.yaml`, not a separate service. GH-21's `classification` field is explicitly OUT of #10's scope — it's a publish-time gate on the shared registry (a different component/moment), #10 only *consumes* labels for its authz decision. Follow-up ticket for that registry publish-gate identified but not filed — Driver's call pending. #10's own sizing unchanged (~1 day, ADR-008 called this additive).
- **GH-24 trial 1 (against #10) succeeded but isn't proof yet**: caught the exact `skills`-array ambiguity above before it got built wrong — real positive kill-criteria evidence, logged on issue #24 as a follow-up needing a second, differently-shaped trial before formalizing into OPERATING-PROTOCOL.md. G0 deliberately NOT ratified — still "drafted."
- Carried forward: GH-17–21 ratified/pushed; GH-22 found a real unfixed template gap (RR-05, "Regulated/reported outputs" doesn't self-identify "LCR"); GH-23 correctly left open (landing condition not met); req-trace.sh is honestly red repo-wide now (needs per-work-item scoping like GH-12 gave gate-check.sh, not filed as an issue yet).
