# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 06-security-compliance — #11's G6 secure-gate-record.md drafted, verdict requested via issue #11 (ADR-012), pending Driver reply |
| Last gate passed | G5 for #11, 2026-08-18 (Driver verdict "Approve" via issue #11 comment, ADR-012; DECISIONS.log) |
| Next gate | G6 for #11 — secure-gate-record.md at docs/harness/changes/GH-11/ ready, threat-model delta appended to GH-8/THREAT-MODEL.md, gate-check.sh G6 GH-11 evidence PRESENT. Verdict requested as an issue #11 comment (ADR-012), reply `Approve`/`Decline` there |
| Active milestone | M2 build + G4 + G5 complete, G6 verdict requested. #8 as a whole: built + reviewed, G6 verdict + real deploy (G7) still ahead |
| Current task | None — holding for Driver's reply on issue #11 (Approve/Decline #11's G6) |
| Blockers | none for #8/#9/#10/#11's pipeline. **ADR-011's self-review bootstrap override is now CLOSED** (trigger #4 fired on #11's G5 — 3rd use with no external review) — any future T2/T3 G5 in this repo needs a real second reviewer, no more self-review, until one is found or ADR-011 is superseded. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **`#11` built, G4, G5 passed; G6 drafted and verdict requested.** `secure-gate-record.md` at `docs/harness/changes/GH-11/`: secret scan clean (push-scoped), dep audit clean (`mcp==2.0.0` + transitive, one non-blocking housekeeping item found — `.venv/bin/pip-audit`'s console-script shebang is stale, worked around via `python3 -m pip_audit`, worth a real fix later), threat-model delta closes the two rows `#10`'s delta left `N/A` pending `#11` (excessive agency, query-leak — both now mechanically tested), one new item named for future audit cycles (`mcp==2.0.0`'s OAuth middleware is a supply-chain trust dependency this repo doesn't own). AI-feature checks are the first ones in this repo that are actually load-bearing rather than N/A — all PASS. `gate-check.sh G6 GH-11` evidence PRESENT. Verdict requested as an issue #11 comment (ADR-012, second use), pending reply.
- **ADR-012 is holding up as a real pattern, not a one-off.** Used twice now in the same session it was written (G5's `Approve`, and G6's request just filed) — both times the AI read the actual comment before logging anything, never inferred from chat.
- **⚠️ ADR-011's bootstrap override is CLOSED — trigger #4 fired on `#11`'s G5.** No future T2/T3 G5 in this repo may self-review until a real second reviewer is found (trigger #1) or ADR-011 is explicitly superseded — load-bearing for whoever runs the next T2/T3 work needing G5. Carried forward, unchanged: `.venv/bin/pip-audit`'s stale shebang (new, this session, repo housekeeping); `#30` still blocks CHANGE.md/T3 and §9 hedge-rule changes; `req-trace.sh` still can't see bare `#NN` IDs (not yet filed); GH-22's RR-05 template gap still open; `#9`'s own G6/threat-model delta was never backfilled.
