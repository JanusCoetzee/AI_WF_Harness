# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 04-implementation — building M1 (#10) per docs/harness/PLAN.md |
| Last gate passed | G5 for #9, 2026-08-18 (self-review under ADR-011 bootstrap override — NOT independent review; DECISIONS.log, review-record.md at docs/harness/changes/GH-9/) |
| Next gate | G4 for #10 (build + verify), once M1's tasks are done |
| Active milestone | M1 — #10 doctrine API + authz interface (docs/harness/PLAN.md; ~1 day; blocks #11 MCP) |
| Current task | Starting #10's build: content-store module (sha256-verified reads), manifest schema (ADR-002 + ADR-008's skills array), authz module (is_allowed(), fail-closed) |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **G3/G5 gate-skip found and closed, not repeated**: asked to "containerize the harness" → clarified to "finish #10/#11" → checked `harness-build`'s own precondition ("G3 in DECISIONS.log") before starting → found #9 was G4-passed 2026-07-19 with **no PLAN.md/G3 ever ratified**. Closed retroactively: `docs/harness/PLAN.md` drafted (M0 #9 retroactive/complete, M1 #10 next, M2 #11 sketched only) and G3-ratified. G5 for #9 also closed via **ADR-011** (new, `docs/harness/adr/ADR-011-g5-bootstrap-override.md`): G5's "must not be the Driver" rule is overridden for T2/T3 work here during single-operator bootstrap — T1 explicitly excluded, 4 named revisit triggers, use-count tripwire at 3 (this is use #1). Review record at `docs/harness/changes/GH-9/review-record.md` — explicitly marked self-review, not independent, top of the file.
- **Now building #10 (M1)** per `PLAN.md`'s task list: content-store module, `GET /api/doctrine/{version}/manifest`+`/file`, authz module. Every future G5 in this repo must cite ADR-011 the same explicit way GH-9's did, or independent review must actually be found — don't let "self-review" quietly stop being labeled as such.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open.
