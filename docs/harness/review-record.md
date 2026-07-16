# Review Record — CHG-001 (G5)

## Reviewer pack (prepared by the AI pair)

| Field | Value |
| --- | --- |
| Change | CHG-001 — /api/health + home-page counts |
| Commit under review | 891e2c2 |
| REQs served | CHG-001.1, .2, .3 (CHANGE.md) |
| Evidence | verify log `evidence/verify-20260717-090031.log` (9 passed); demo `changes/CHG-001/demo-record.txt` |
| Demo | `curl http://127.0.0.1:5052/api/health` → `{"documents":31,"skills":13,"status":"ok"}` |
| Area of least confidence | semantics of the "documents" count (see finding 2) |

## AI adversarial self-review (input to G5 — approves nothing)

Hunted for: plausible-but-wrong, test theater, invented APIs, unvalidated
boundaries, REQ drift, weakened assertions. Findings ranked:

| # | Severity | Finding | Failure scenario | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Low | Count computation duplicated in `index()` (server.py:124) and `api_health()` (server.py:157-161) | The two drift under a future edit and CHG-001.2 ("same counts") silently breaks — the cross-check test (`test_health_counts_match_catalog`) covers API↔catalog but UI↔API is only cross-checked via `test_home_hero_shows_counts`, which WOULD catch drift; risk is therefore maintenance cost, not silent breakage | Fix now: extract `_counts()` helper (small verified commit) |
| 2 | Info | "documents" count includes the config entry (harness.config.yaml) — 31 includes 1 YAML file | An operator reading "31 documents" assumes 31 markdown docs | Accept: counts describe catalog entries; noted here for the record |
| 3 | Info | Characterization pin for /api/health 404 was changed in the same commit as the feature | By design (recon note said the change commit must move the pin) — visible in diff, deliberate | Accept |
| — | — | Checked and clean: no weakened assertions; no invented Flask APIs (test_client, get_json verified against installed Flask 3.1.3); no REQ-less hunks (all 15 app lines serve CHG-001.1/.2); no unvalidated external input (endpoint takes none) | | |

## Traceability spot-check (3 of 3)

| REQ | Walks to |
| --- | --- |
| CHG-001.1 | app/server.py `api_health()` → tests/test_health.py::test_health_returns_ok_with_counts, ::test_health_counts_match_catalog ✓ |
| CHG-001.2 | app/templates/index.html hero → tests/test_health.py::test_home_hero_shows_counts ✓ |
| CHG-001.3 | tests/test_characterization.py (6 pins, one deliberately moved with in-diff comment) ✓ |

## Human review (T2: one reviewer required)

| Reviewer | Verdict | Date |
| --- | --- | --- |
| janus (SIMULATED — e2e drill; a real G5 requires a human independent of the Driver) | Approve with finding 1 fixed | 2026-07-17 |

Diff size: 15 lines of app code + tests/docs — within the ~500-line ceiling.
