# Review Record — #10 (G5)

**This is a self-review under ADR-011's bootstrap override, not an
independent review.** Same notice as `GH-9`'s: `gates/GATES.md`'s G5 rule
states the reviewer "must not be the Driver" — no second reviewer is
available to this repo yet. This is **use #2 of 3** toward
[`ADR-011`](../../adr/ADR-011-g5-bootstrap-override.md)'s trigger #4
tripwire (three overrides used without any external review ever
occurring) — recorded here so the count stays visible, not just in
`DECISIONS.log`.

## Reviewer pack

| Field | Value |
| --- | --- |
| Change | #10 — doctrine API + authz interface (M1) |
| Commits under review | `e38c19d` (build), plus this review's own fix commit (see below) |
| Tier | T2 |
| Evidence | 59 tests green (was 57 at G4 — 2 added during this review), `app/doctrine.py` 92% / `app/server.py` 97% coverage, ruff clean, `pip-audit` clean (`PyYAML==6.0.3`) |
| Demo | `curl -s "localhost:5050/api/doctrine/harness-v0.2/manifest" \| python3 -m json.tool \| head` (`PLAN.md` M1) — re-run below alongside the failure-mode probe |
| Area of least confidence | Content-store correctness under an atypical `HARNESS_ROOT` (not the happy-path repo checkout the demo and #9's own docker proof both use) |

## Adversarial self-review (input to G5 — approves nothing on its own)

Hunted for: plausible-but-wrong claims, invented APIs, unvalidated
boundaries, weakened assertions, scope creep. Unlike `GH-9`'s review, this
one didn't stop at reading the diff — it ran the code against a
deliberately hostile input (a `HARNESS_ROOT` with no `.git`) before writing
any of this up, because "solid foundation" means demonstrated, not
asserted.

| # | Severity | Finding | Failure scenario | Disposition |
| --- | --- | --- | --- | --- |
| 1 | **Real — fixed in this review** | `_git_commit()` called `subprocess.run(..., check=True)` with no exception handling. A `HARNESS_ROOT` with no `.git` (a stripped content bundle, or a minimal image missing the `git` binary — both plausible under ADR-008's published-tag model, not a contrived edge case) made `build_manifest()` raise `CalledProcessError`, uncaught, on **every single request** to either doctrine route | Reproduced live before fixing: `doctrine.build_manifest()` against a no-`.git` root crashed with an unhandled traceback; through the Flask route this surfaced as a generic 500, but via the *unhandled-exception* path, not the documented fail-closed contract — server logs got a raw subprocess traceback (including the real filesystem path) on every request, and nothing about the failure mode was tested | **Fixed**: `app/doctrine.py` gained `ManifestBuildError`, `_git_commit()` catches `CalledProcessError`/`FileNotFoundError` and raises it; `app/server.py::_build_manifest_or_404` catches it and returns a clean, documented 500; `scripts/doctrine-manifest.py` catches it too (clean stderr + non-zero exit). Two new regression tests (`test_g5_no_git_root_*`) pin both the module and route behavior. Re-verified: `verify.sh` ALL GREEN, 59 tests |
| 2 | Info | `build_manifest()` recomputes a sha256 for every catalogued file (~52 currently) and shells out to `git rev-parse HEAD`, on **every** manifest/file request — no caching. Not wrong (correctness > perf for this slice, and the ticket didn't scope caching), but it's a real repeated-request cost and a mild DoS surface once this is behind a real ALB | Accept for this slice — same category as `GH-9`'s accepted info findings (a real gap named, not hidden). Worth revisiting when `#11`'s MCP tools add call volume, or before this moves off single-operator bootstrap |
| 3 | Info | `is_allowed()`'s v1 policy make every item's `classification` uniformly `"Internal"` — the fail-closed *mechanism* is real and tested (finding a genuinely unlabeled/unrecognized item denies), but there's currently no code path that produces a non-`"Internal"` label to exercise real differentiation end-to-end. Correct per `#10`'s own scope (GH-21's publish-time classification gate is explicitly out of scope) | Accept — named as a forward pointer to GH-21, not a gap in `#10` itself |
| 4 | — | Checked and clean: path-traversal on `/api/doctrine/{version}/file?path=...` is closed by construction (exact-match lookup against the manifest's own allowlist, not filesystem-relative resolution) — confirmed by tracing `api_doctrine_file`'s lookup, not just asserted; `is_allowed()`'s default `policy` argument is a module-level dict of empty lists, read-only at call time, no shared-mutable-default bug | | Accept |

## Traceability spot-check (manual — `req-trace.sh` limitation, sharper here than GH-9's)

`scripts/req-trace.sh` scans for IDs matching `[A-Z][A-Z0-9]+-[0-9]+` — a
bare `#10` (this repo's actual GitHub-issue-number convention for `#8`'s
slices) doesn't match that shape at all, so this work item is
**structurally invisible** to the tool, not just unscoped to one item
(`GH-9`'s milder version of the same landmine). Confirmed by running it:
36 unrelated failures, no row for `#10`. Still not filed as its own issue
— flagging again, now with the sharper detail, rather than re-deferring
silently.

| Claim | Traces to |
| --- | --- |
| Manifest schema (ADR-002 + ADR-008 `skills[]`) | `app/doctrine.py::build_manifest`, `tests/test_doctrine_api.py::test_10_1_manifest_matches_schema` + `test_10_5_skills_report_exactly_the_config_pin` ✓ |
| No `latest`/versionless route, 404 unknown version | `app/server.py` route table (only `<version>` segments defined), `test_10_3_*` ✓ |
| 500 (never content) on tamper | `app/doctrine.py::read_file_verified` (raises `IntegrityError`), `app/server.py::api_doctrine_file` (catches, `abort(500)`), `test_10_2_*` ✓ |
| Fail-closed authz, unlabeled/unrecognized denied | `app/doctrine.py::is_allowed`, `test_10_4_*` ✓ |
| `scripts/doctrine-manifest.py` runnable in CI | `.github/workflows/*.yml` already runs `scripts/verify.sh` → `pytest tests/`, which now includes `test_doctrine_manifest_script_runs_clean` / `..._nonzero_exit_on_unknown_version` exercising the actual CLI subprocess, not just the importable module ✓ |
| `HARNESS_ROOT` failure mode is fail-closed, not a crash | `app/doctrine.py::ManifestBuildError`, `app/server.py::_build_manifest_or_404`, `test_g5_no_git_root_*` ✓ (finding #1 above) |

This is still a real, if smaller, gap versus a proper G5 with a working
`req-trace.sh` — flagged, not hidden, same as `GH-9`'s.

## Human review (T2: one reviewer required — see override notice at top)

The adversarial self-review above is AI-drafted input to this gate — it
approves nothing on its own (CLAUDE.md §7: "a gate's 'review passed'
condition is met only by a human"; ADR-011 waives G5's *independent-
reviewer* requirement, not who gets to render the verdict).

| Reviewer | Verdict | Date |
| --- | --- | --- |
| janus (Driver — self-review under ADR-011 override, NOT an independent reviewer) | Approve | 2026-08-18 |

Diff size (this review's fix, on top of `e38c19d`): `app/doctrine.py`,
`app/server.py`, `scripts/doctrine-manifest.py`, `tests/test_doctrine_api.py`
— small, targeted, within the ~500-line ceiling.
