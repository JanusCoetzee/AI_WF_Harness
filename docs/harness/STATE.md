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
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **Harness vendored into AU_YEAR_9_MATH (real external adoption) produced real feedback**: CHG-001 there hit a genuine failure (unresolved "markdown or HTML" hedge survived GC, cost a post-G4 rebuild) — retro at `docs/RETROS/RETRO-2026-08-18.md`. Fixed upstream here as GH-26 (gate-check.sh false-positive on `CHG-###` in prose — real regression test, `tests/test_gate_check.py`, 15 cases, wired into verify.sh permanently), GH-27 (CHANGE.md delivery-medium prompt), GH-28 (T3-light CHANGE.md fields, design decided in ADR-010), GH-29 (CLAUDE.md §9 hedge rule, ported from the field-tested downstream copy). All four GC-ratified and pushed.
- **#30 is a live blocker** (see top Blockers field): GH-27/28/29 are prompt/template/constitution changes with zero durable eval coverage — only evidence they work is the one incident that motivated them. #30 has detailed acceptance criteria for the blind-authored scenario needed to close this (I'm disqualified as author, same reasoning as GH-16/GH-22's recusals). Don't touch CHANGE.md's delivery-medium/T3 logic or CLAUDE.md §9's hedge rule again until #30 lands.
- Carried forward, still true: **#10 redefined and ready to build** (skills array in scope per ADR-008, GH-21's classification field explicitly out of scope — see #10's GitHub body, rewritten 2026-08-12). **GH-24** trial 1 succeeded but needs a second trial before formalizing (issue #24, still open). req-trace.sh is honestly red repo-wide (not filed as an issue). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification) — still open.
