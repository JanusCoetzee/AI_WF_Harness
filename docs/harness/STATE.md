# STATE — harness working state

Machine-readable-ish session anchor. The LLM reads this first every session; keep it
current — a stale STATE.md is worse than none.

| Field | Value |
| --- | --- |
| Work item | #8 — central doctrine service on ECS (browser + MCP) |
| Risk tier | T2 |
| Current stage | 06-security-compliance next — M1 (#10) build + G4 + G5 all passed; #11 (M2) not yet decomposed |
| Last gate passed | G5 for #10, 2026-08-18 (self-review under ADR-011 bootstrap override — NOT independent review; use #2 of 3 toward its trigger #4 tripwire; Driver verdict: Approve; review-record.md at docs/harness/changes/GH-10/) |
| Next gate | G6 for #10 (secure-gate-record: secret scan, dep audit, threat-model delta, data sweep) — not started. Or: decompose #11 (M2) to task level first, PLAN.md's call |
| Active milestone | M1 complete (build + G4 + G5). M2 — #11 MCP tools not yet decomposed to task level |
| Current task | None — holding for direction: G6 for #10, or decompose #11 |
| Blockers | none for #8/#9/#10's pipeline. #30 (open) BLOCKS further changes to templates/CHANGE.md's delivery-medium/T3-collapse logic (GH-27/28, ADR-010) or CLAUDE.md §9's hedge rule (GH-29) until a blind-authored eval scenario proves they actually work — see handoff |
| UNVERIFIED items | none |

## Session handoff notes

Three bullets max, overwritten each session-end: what just happened, what's next,
any landmine the next session must know about.

- **#10 (M1) built, G4 passed, G5 passed**: `app/doctrine.py` (content-store, authz), `app/server.py` doctrine routes, `scripts/doctrine-manifest.py`, `harness.config.yaml`'s `doctrine:` pin. The adversarial self-review found and **fixed** a real bug before writing it up (not after): `_git_commit()` crashed unhandled (raw `CalledProcessError`) on any `HARNESS_ROOT` with no `.git` — reproduced live, fixed with `ManifestBuildError` caught cleanly at both the route and CLI layers, pinned by 2 new tests. 59 tests green, 95% coverage. Driver's explicit in-session verdict: Approve. Review record: `docs/harness/changes/GH-10/review-record.md`. **This is use #2 of 3** toward ADR-011's trigger #4 tripwire — one more self-reviewed G5 without ever finding external review ends the bootstrap override per its own terms.
- **Next choice**: G6 (secure-gate-record) for `#10`, or decompose `#11` (MCP tools, M2) to task level — `PLAN.md` says do the latter once `#10` is G4-complete, which it now is (and G5-complete too).
- Carried forward: **#30 is a live blocker** (top Blockers field) — no CHANGE.md delivery-medium/T3 or CLAUDE.md §9 hedge-rule changes until it lands. **GH-24** needs a second trial (issue #24, open). `req-trace.sh` is honestly red repo-wide, not scoped per-item (not yet filed). GH-22 found an unfixed template gap (RR-05, "LCR" self-identification), still open.
