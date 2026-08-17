# PLAN — #8 Central harness doctrine service (ECS: browser + MCP)

| Field | Value |
| --- | --- |
| Status | **Ratified (G3)** — 2026-08-18. Retroactive for M0, prospective for M1/M2 (see Plan change log) |
| Re-planning checkpoint | N/A — three-milestone plan, each ~1 day, under the 2-week threshold |
| PRD | N/A — #8 entered at G2 directly (escalation trigger: new external interface), per `DECISIONS.log` 2026-07-19. `ADR-002-central-doctrine-service.md` and its RBAC amendment carry the requirements a PRD would otherwise hold |

## Milestone map

Sequenced riskiest-assumption-first, per the three ADR-002 layers (doctrine
central / enforcement local / evidence in-repo — the split this whole
service exists to prove out).

| # | Milestone (behavior, not component) | Demo command | Proves / kills which risk |
| --- | --- | --- | --- |
| M0 | Walking skeleton: harness content served read-only from a container, integrity-of-deployment proven (`docker --read-only`, non-root, healthy) | `docker run --rm --read-only -p 5050:5050 -v $(pwd):/harness:ro -e HARNESS_ROOT=/harness harness-browser` | Kills the biggest unknown first: can the harness's doctrine actually be served from a container under ADR-002's fail-closed/read-only posture at all, before building any API contract on top of it |
| M1 | Doctrine content addressable by explicit version with cryptographic integrity, plus the authz interface (`is_allowed()`) ADR-002's RBAC amendment requires | `curl -s "localhost:5050/api/doctrine/harness-v0.2/manifest" \| python3 -m json.tool \| head` (per `#10`'s own Proof section) | Proves the actual machine contract — explicit-version-only, fail-closed sha256, fail-closed authz — works before any client (human or MCP) depends on it |
| M2 | IDE sessions can pull doctrine through read-only MCP tools with provenance (`#11`) | TBD — sketched only, not yet ticketed to the same detail as M1; `#11`'s own issue will carry the real demo command when drafted | Proves the actual consumption path (an LLM session fetching gates/templates live instead of vendoring them) works end to end — the whole reason M0/M1 exist |

## Milestone detail

### M0 — Container walking skeleton (#9) — COMPLETE, G4 passed 2026-07-19

- **Tasks** (as actually done, captured retroactively from commit `3387c01`):
  - [x] T0.1 — `_resolve_root()`: `HARNESS_ROOT` env root for container mode, local-dev behavior pinned unchanged
  - [x] T0.2 — `Dockerfile`: `python:3.12-slim`, non-root user, `HEALTHCHECK` on `/api/health`, gunicorn with `/dev/shm` worker tmp so the container runs fully `--read-only`
  - [x] T0.3 — `pip-audit` clean on pinned `requirements.txt` (STD-004)
- **Test strategy:** red-first (`tests/test_container.py`, 2 red before `_resolve_root()` existed); 21 tests green, 98% coverage at G4.
- **Demo command:** `docker run --rm --read-only -p 5050:5050 -v $(pwd):/harness:ro -e HARNESS_ROOT=/harness harness-browser`
- **Demo record** (from commit `3387c01`'s own verified claims, `DECISIONS.log` 2026-07-19 G4-passed line):

```text
21 tests green, 98% cov. Docker proof run healthy with repo mounted :ro;
write attempts refused on both mount and root fs. pip-audit on pinned
requirements clean (STD-004).
```

- G5 review of this milestone is still pending (human) — noted here, not
  hidden: M0 is *built and G4-verified*, not yet reviewed. Building M1 on
  top of it is a deliberate call (same one implicitly already made when M0
  shipped without a ratified G3) — not a claim that M0 is fully closed out.

### M1 — Doctrine API + authz interface (#10)

- **Tasks:** per `#10`'s own ticket body (already redefined 2026-08-12 —
  `skills` array confirmed in scope per ADR-008, GH-21's classification
  field confirmed out of scope):
  - [ ] T1.1 — Content-store module: sha256-verified reads, manifest schema per ADR-002 extended with ADR-008's `skills` array
  - [ ] T1.2 — `GET /api/doctrine/{version}/manifest` and `GET /api/doctrine/{version}/file` — no `latest`, 404 unknown version, 500 on hash mismatch
  - [ ] T1.3 — Authz module `is_allowed(identity, item) -> bool`, v1 allow-all-authenticated, fail-closed on missing/unrecognized classification label
  - [ ] T1.4 — `scripts/doctrine-manifest.py`, runnable in CI
- **Test strategy:** `tests/test_doctrine_api.py` — schema validation incl. `skills[]`, tamper test (500 not content), authz test (unlabeled → denied). Per `#10`'s Verify section: coverage ≥80% on changed lines, ruff clean.
- **Demo command:** `curl -s "localhost:5050/api/doctrine/harness-v0.2/manifest" | python3 -m json.tool | head`
- **Demo record** (filled at completion — paste observed output):

```text
(observed output here — this is G4 evidence)
```

### M2 — MCP tools (#11)

- **Tasks:** not yet decomposed to task level — `#11` isn't ticketed with
  `#10`'s level of detail yet (blocked on `#10` landing first; ADR-002's
  MCP tool table, `harness_get_template` etc., is the design starting
  point). Decompose properly when `#10` is G4-complete, don't speculate now.
- **Test strategy:** TBD at `#11`'s own ticketing.
- **Demo command:** TBD.
- **Demo record:** N/A — not started.

## Out-of-plan proposals

| Date | Proposal | Disposition (PRD change / next cycle / rejected) |
| --- | --- | --- |
| 2026-08-12 | GH-21: per-skill `classification` field on the shared registry's publish-time gate | Explicitly scoped OUT of M1/`#10` (different component/moment — registry publish vs. `#10`'s read-side API); real work, not yet ticketed. Driver's call pending (`DECISIONS.log` 2026-08-12) |
| 2026-08-12 | Cross-repo recon/ADR retrieval via the doctrine service (semantic search over `docs/harness/**`) | Deliberately deferred — `DECISIONS.log` 2026-07-25 says "premature ahead of #8/#10-#11 landing," reaffirmed as GitHub issue #23 (scope-checked, correctly left open — landing condition still not met) |

## Plan change log

Plans change deliberately, not silently.

| Date | Change | Reason | Approved by |
| --- | --- | --- | --- |
| 2026-08-18 | Plan drafted retroactively for M0 (already shipped/G4-passed), prospectively for M1/M2 | `#9` was built and `G4`-passed without a ratified G3/PLAN.md ever existing — a real gate-skip in `#8`'s own history, found while checking `harness-build`'s own stated precondition ("G3 in DECISIONS.log") before starting `#10`. Closing the gap before building a second slice on the same unratified foundation, not building `#11` on top of two skipped gates | pending Driver G3 ratification |
