# Review Record — #9 (G5)

**This is a self-review under ADR-011's bootstrap override, not an
independent review.** `gates/GATES.md`'s G5 rule states the reviewer "must
not be the Driver" — this repo currently has one operator and no second
reviewer available, so this review is being conducted and logged as an
explicit, named exception (`docs/harness/adr/ADR-011-g5-bootstrap-override.md`),
not silently presented as if independent review occurred. Anyone reading
this later: do not count this as satisfying G5's independent-review
guarantee for any purpose beyond this repo's own T2/T3 bootstrap.

## Reviewer pack

| Field | Value |
| --- | --- |
| Change | #9 — containerize the harness browser |
| Commit under review | `3387c01` |
| Tier | T2 |
| Evidence | 21 tests green, 98% coverage; docker proof run healthy with repo mounted `:ro`, write attempts refused on both mount and root fs; `pip-audit` on pinned `requirements.txt` clean (STD-004) — all per the commit's own message and `DECISIONS.log`'s 2026-07-19 G4-passed line |
| Demo | `docker run --rm --read-only -p 5050:5050 -v $(pwd):/harness:ro -e HARNESS_ROOT=/harness harness-browser` (`docs/harness/PLAN.md` M0) |
| Area of least confidence | The container has not been run under a hostile/adversarial network posture (no SSO/ALB in front of it yet — out of scope for this slice, `Dockerfile`'s own header says content is a read-only volume mount, app carries no auth) |

## Adversarial self-review (input to G5 — approves nothing on its own)

Hunted for: plausible-but-wrong claims, invented APIs, unvalidated
boundaries, weakened assertions, scope creep.

| # | Severity | Finding | Failure scenario | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Info | `_resolve_root()`'s env-var fallback (`HARNESS_ROOT`) is trusted without validation — a malformed/absolute-path-outside-mount value isn't rejected | Container is deployed with a misconfigured `HARNESS_ROOT`; content served would be whatever's at that path, not necessarily the intended harness mount — low severity since this is operator-supplied config at deploy time, not attacker-reachable input | Accept for this slice; worth a bounds-check when `#10` builds real path handling on top of this (`content-store module` in `PLAN.md` M1) |
| 2 | Info | No test exercises the container under a genuinely read-only filesystem with a non-writable `/tmp` (the `/dev/shm` worker-tmp workaround is asserted correct by the `Dockerfile` comment, not verified by an automated test) | If a future base-image change removes `/dev/shm` availability, this would silently break and only be caught by the manual `docker run --read-only` proof, not CI | Accept — same class of gap noted for `gate-check.sh`/`audit-decisions.sh` all session (manual verification only); not blocking, but a real gap worth naming rather than ignoring |
| 3 | — | Checked and clean: `Dockerfile` matches its own documented invariants (non-root `USER harness`, `HEALTHCHECK` against the real `/api/health` endpoint, no secrets baked into the image); `.dockerignore` excludes `.git`/`.venv`/dev artifacts from the build context | | Accept |

## Traceability spot-check (manual — `req-trace.sh` limitation noted)

`scripts/req-trace.sh` cannot be used here as designed: it traces every
`REQ-###`/`GH-##.#` ID across the **whole repo**, not scoped to one work
item (`STATE.md`'s own landmine, not yet filed as an issue). Running it
returns 36 unrelated failures from other work items, not a #9-specific
signal. Manual spot-check instead, same style G5 used before `req-trace.sh`
existed (ADR-005):

| Claim | Traces to |
| --- | --- |
| Container runs fully `--read-only` | `Dockerfile`'s `/dev/shm` worker-tmp comment + commit `3387c01`'s "docker proof run healthy... write attempts refused" claim ✓ |
| `HARNESS_ROOT` env root works, local dev unchanged | `app/server.py::_resolve_root()`, `tests/test_container.py` (2 red before implementation, per commit message) ✓ |
| `pip-audit` clean | `STD-004` in `harness.config.yaml`; commit message states pinned `requirements.txt` checked clean at the time ✓ |

This is a real, if smaller, gap versus a proper G5 — flagged, not hidden.

## Human review (T2: one reviewer required — see override notice at top)

| Reviewer | Verdict | Date |
| --- | --- | --- |
| janus (Driver — self-review under ADR-011 override, NOT an independent reviewer) | Approve, with findings 1/2 accepted as-is and the manual-traceability gap (above) explicitly noted, not silently substituted for `req-trace.sh` | 2026-08-18 |

Diff size: `Dockerfile` + `app/requirements.txt` + `app/server.py` changes — within the ~500-line ceiling (`git show 3387c01 --stat`).
