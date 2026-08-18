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

### M1 — Doctrine API + authz interface (#10) — COMPLETE, G4+G5+G6 passed 2026-08-18

- **Tasks:** per `#10`'s own ticket body (already redefined 2026-08-12 —
  `skills` array confirmed in scope per ADR-008, GH-21's classification
  field confirmed out of scope):
  - [x] T1.1 — Content-store module: sha256-verified reads, manifest schema per ADR-002 extended with ADR-008's `skills` array (`app/doctrine.py`: `build_manifest()`, `sha256_of()`)
  - [x] T1.2 — `GET /api/doctrine/{version}/manifest` and `GET /api/doctrine/{version}/file` — no `latest`, 404 unknown version, 500 on hash mismatch (`app/server.py::api_doctrine_manifest`/`api_doctrine_file`)
  - [x] T1.3 — Authz module `is_allowed(identity, item) -> bool`, v1 allow-all-authenticated, fail-closed on missing/unrecognized classification label (`app/doctrine.py::is_allowed`); identity via a documented header stub (`X-Harness-Actor`) — real SSO/OIDC is out of scope per `#10`
  - [x] T1.4 — `scripts/doctrine-manifest.py`, runnable in CI (standalone, no Flask server needed; non-zero exit + stderr on an unknown version)
- **Test strategy:** `tests/test_doctrine_api.py` — 12 tests: schema validation incl. `skills[]` (AC1), skills[] matches the config pin exactly (AC5), tamper detection at both the module and route layers (AC2), no-`latest`/unknown-version 404 (AC3), fail-closed authz incl. unlabeled-item-under-a-restrictive-policy and unauthenticated-denied (AC4). Manual schema assertions, not the `jsonschema` package — the schema is small/stable, not worth a new pinned dependency. Coverage: `app/doctrine.py` 91%, `app/server.py` 96% (≥80% threshold met); ruff clean.
- **Demo command:** `curl -s "localhost:5050/api/doctrine/harness-v0.2/manifest" | python3 -m json.tool | head`
- **Demo record** (observed 2026-08-18, `scripts/verify.sh --log` → `docs/harness/evidence/verify-20260818-094129.log`, ALL GREEN, 55 tests):

```text
$ curl -s -H "X-Harness-Actor: janus" "localhost:5050/api/doctrine/harness-v0.2/manifest" | python3 -m json.tool | head -20
{
    "files": [
        {
            "classification": "Internal",
            "kind": "doc",
            "path": "README.md",
            "sha256": "42436d812f93310ab849f45c387bc4bf01c433a99fd2fd13d8ed84253b8612e1",
            "title": "AI Workflow Harness"
        },
        ...
    ],
    "git_commit": "fd734aba5f8ec9e472bca1372345b589490dab7f",
    "skills": [
        {"name": "harness-issues", "version": "harness-v0.2"},
        {"name": "harness-build", "version": "harness-v0.2"},
        {"name": "harness-release", "version": "harness-v0.2"}
    ],
    "version": "harness-v0.2"
}

$ curl -s -o /dev/null -w "%{http_code}\n" "localhost:5050/api/doctrine/harness-v99.9/manifest"
404

$ curl -s "localhost:5050/api/doctrine/harness-v0.2/manifest" | python3 -m json.tool   # no X-Harness-Actor
{"files": [], "git_commit": "...", "skills": [...], "version": "harness-v0.2"}   # fail-closed: unauthenticated sees no files
```

All 5 acceptance criteria (`#10`'s ticket body) verified live, not just by unit test: AC1 (schema), AC2 (tamper → 500, confirmed no altered content in body), AC3 (no bare/`latest` route, unknown version → 404), AC4 (unauthenticated → empty `files[]`, fail-closed), AC5 (`skills[]` above matches `harness.config.yaml`'s `doctrine.skills` pin exactly).

### M2 — MCP tools (#11)

- **Tasks:** per `#11`'s own ticket body (redefined 2026-08-18 — transport
  hedge resolved to HTTP-only, `skills[]` confirmed out of scope, same
  style as `#10`'s 2026-08-12 pass):
  - [ ] T2.1 — MCP server process (`app/mcp_server.py`): `MCPServer`,
    `streamable-http` transport only, imports `app/doctrine.py` directly
    (no HTTP hop to `#10`'s own routes — same in-process content-store +
    `is_allowed()` calls)
  - [ ] T2.2 — Stub `TokenVerifier` mirroring `#10`'s `X-Harness-Actor`
    header stub (bearer-token presence = authenticated, no real OIDC);
    feeds `is_allowed(identity, item)` unchanged from `#10`
  - [ ] T2.3 — Four tools per ADR-002's table: `harness_get_template`,
    `harness_get_gate`, `harness_get_standard`, `harness_search_doctrine`
    (ranked title/heading/excerpt match over `files[]` only); every
    response carries `{version, path, sha256}` provenance; unknown version
    → tool error, never silent fallback
  - [ ] T2.4 — README sample client config
    (`claude mcp add --transport http harness-doctrine <url>`)
- **Test strategy:** `tests/test_mcp_doctrine.py` — schema-validated tool
  responses, provenance on every response, exactly 4 tools registered (no
  stdio, no write tools), tamper → tool error not content, denial → tool
  error not content (reuses `#10`'s `is_allowed()` test patterns). Per
  `#11`'s Verify section: coverage ≥80% on changed lines, ruff clean.
- **Demo command:**
  ```bash
  .venv/bin/python -m pytest -q tests/test_mcp_doctrine.py
  # then live: claude mcp add --transport http harness-doctrine <endpoint>/mcp
  # ask a session: "fetch the CHANGE template at harness-v0.2 via harness_get_template"
  ```
- **Demo record** (filled at completion — paste observed output):

```text
(observed output here — this is G4 evidence)
```

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
| 2026-08-18 | M1 (`#10`) built, verified, G4 passed | All 4 tasks done, all 5 acceptance criteria met by test + live demo, `verify.sh` ALL GREEN | janus (in-session) |
