# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 05-review — M1 (#10) complete, G4 passed; #11 (M2) not yet decomposed |
| Last gate passed | G4 for #10, 2026-08-18 (in-session Driver approval; DECISIONS.log) |
| Next gate | G5 for #10 — review record needed; ADR-011 override applies (use #2 of 3 toward its trigger #4 tripwire if used again as self-review) |
| Active milestone | M1 complete. M2 — #11 MCP tools not yet decomposed to task level (docs/harness/PLAN.md's own note: do it once #10 is G4-complete, which it now is) |
| Current task | None — holding for direction: decompose #11, or do #10's G5 review first |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) built and verified**: `app/doctrine.py` (content-store — `sha256_of`/`build_manifest`/`read_file_verified`, `is_allowed()` fail-closed authz), new routes on `app/server.py` (`GET /api/doctrine/{version}/manifest`+`/file`), `scripts/doctrine-manifest.py` (standalone, CI-runnable), `harness.config.yaml` gained a `doctrine:` composition pin (ADR-008's `core_version`+`skills[]`). `tests/test_doctrine_api.py`: 12 tests, all 5 acceptance criteria from `#10`'s ticket body covered. `verify.sh` ALL GREEN (55 tests, 95% cov), `pip-audit` clean on the one new dependency (PyYAML). Demo command run live, not just unit-tested — output in `PLAN.md`'s M1 demo record. **G4 not yet marked passed** — GATES.md names Driver as G4's approver, not AI; this session ended the build handing off for that approval, per the same segregation-of-duties discipline ADR-011 exists to protect rather than quietly erode.
- **Next up once G4 is approved**: decompose `#11` (MCP tools, M2) to `#10`'s level of ticket detail — deliberately not done yet, `PLAN.md` says so. Every future G5 in this repo must cite ADR-011 the same explicit way GH-9's did, or independent review must actually be found — don't let "self-review" quietly stop being labeled as such.
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open.
