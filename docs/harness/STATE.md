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
| Active milestone | #10 doctrine API + authz interface (~1 day; blocks #11 MCP) |
| Current task | #9 done+proven; awaiting review or go on #10 |
| Blockers | none |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- GH-17..GH-21 independently re-verified in a separate session and GC-ratified: req-trace.sh recognizes GH-##.# IDs (correctly now fails repo-wide — real gaps, see landmine below), gate-check.sh catches bold **Yes**, audit-decisions.sh gained a chronology check + gh-issue-state cross-check (both reproduced against synthetic copies of the exact bugs they catch), THREAT-MODEL.md's ADR-008 risks #6/#7 have named revisit triggers. All five dossiers now "Ratified (GC)"; DECISIONS.log has the GC passed line. Committed + pushed.
- GH-22: outside-author GT rewrite applied to regreport, kept under ground-truth/pending/ (not promoted) — real gap found (RR-05: "Regulated / reported outputs" never self-identifies "LCR"), filed in REPORT.md as a template gap, not yet fixed. GH-23 scope-checked, correctly left open (its own landing condition not met).
- Next: #10 doctrine API+authz (blocks #11 MCP) — ADR-008 supersedes ADR-002's single-shared topology; #10's manifest schema MUST add a `skills` array, and per GH-21's mitigation proposal consider a per-skill `classification` field at the same time (cheaper now than retrofitting). Landmine: no "latest" doctrine endpoint ever (ADR-002); version drift across BU instances is a human function, not harness-enforced (ADR-008). New landmine: req-trace.sh is now honestly red repo-wide (sub-criteria ids aren't cited verbatim in commit messages by convention) — needs per-work-item scoping like gate-check.sh got in GH-12, or G5 reviews will hit a wall of unrelated historical noise; not filed as an issue yet, Driver's call whether it's worth one.
