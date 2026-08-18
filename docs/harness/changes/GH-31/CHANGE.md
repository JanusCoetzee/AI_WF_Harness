# CHANGE — #31 Both harness-doctrine processes run together in one proven Docker container

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #31 — scoped 2026-08-18 after "how far are we from a container" surfaced that `#11` was never containerized |
| Date | 2026-08-18 |
| Risk tier | T2 — internal deploy tooling; no customer data, no new external interface (same content/contracts `#9`/`#10`/`#11` already shipped and G6-cleared) |
| Recon | required — see `RECON.md` |
| Linked records | `#9` (browser container, precedent for the read-only/non-root posture reused here), `#11` (MCP process, depended on, done) |
| Timing constraints | none — local tooling, no freeze windows |
| Constitution sections consulted | §2 (verify loop — this ticket's proof is a live, reproduced run, not an assertion), §8 (brownfield — understand before changing; RECON.md's implicit-contract table), §9 (an AC that turned out to assume something the platform doesn't support gets corrected here, in the open, not quietly reinterpreted at build time) |

## Intent

`#11`'s MCP process has never run inside Docker — every gate it passed was verified against a bare local process. Done means one image, built from the existing `Dockerfile`, runs both the browser and the MCP endpoint, both externally reachable, both proven live under `--read-only`/non-root, with `#11`'s own MCP demo sequence re-run successfully against the containerized endpoint.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-31.1 | Given `docker build`, when run via `docker run --rm --read-only -p 5050:5050 -p 5051:5051 ...`, then both the browser (`5050`) and the MCP endpoint (`5051`) are reachable from outside the container |
| GH-31.2 | Given the running container, when `/api/health` is polled, then `200` (unchanged, regression-proofed) |
| GH-31.3 | Given the running container, when its `HEALTHCHECK` runs, then it checks both processes (an HTTP `GET /api/health` for the browser, a TCP-connect probe for MCP) and reports which one failed in its own output if either is down — not a silent single bit with no diagnostic |
| GH-31.4 | Given the container running under `--read-only`, when the MCP process handles a request, then it does not crash or fail from an attempted filesystem write (verified live; `RECON.md` also confirms no writes exist in the `mcp` package's own source) |
| GH-31.5 | Given the containerized MCP endpoint, when `#11`'s own live demo sequence is re-run against it (`initialize` → `tools/list` → `tools/call`, unauthenticated request still `401`s at the transport layer), then it succeeds identically to the bare-process proof already on record in `PLAN.md` |
| GH-31.6 | **(Narrowed from the original ticket per RECON.md's finding — Docker's `HEALTHCHECK` is one bit per container, not two independent signals.)** Given both processes running, when one is killed, then the surviving process keeps actually serving traffic (verified live: kill one, curl the other, get a real response) — the container's overall health bit still goes unhealthy (that's correct, not a defect: this repo's own `THREAT-MODEL.md` control-failure-semantics table already treats container-level availability as "open by design," an orchestrator restarting the whole task on unhealthy is consistent with that, not new) |
| GH-31.7 | Given the built image, when inspected, then both processes run as the existing non-root user (`uid 10001`) — no privilege escalation introduced to solve process supervision |

## Remediation of past impact

Live testing for this ticket found a real, previously-undetected defect in
`#10`'s **already-shipped, already-G4/G5/G6-passed** manifest route, not
just in `#11`'s new one: `app/doctrine.py::_git_commit()` shells out to
`git rev-parse`, and the `python:3.12-slim` base image never had `git`
installed. Every manifest-serving call (`#10`'s HTTP route *and* `#11`'s
MCP tools — same shared code) would have raised `ManifestBuildError` inside
the real container, 100% of the time, since `#10` first shipped. This was
invisible until now because neither `#10`'s nor `#11`'s G4/G5/G6 evidence
was ever gathered against the actual container — both ran against bare
local processes, where a developer machine's `git` was on `PATH` by
coincidence, not by design.

Checked `DECISIONS.log`: no prior G4/G5/G6 passage for `#10` or `#11` cited
a containerized run as its evidence, so this defect was never exercised in
anger, let alone shipped to a real user — the same "found before it did
damage" disposition `GH-12`'s own remediation note used. Disposition:
**forward-only fix**, applied here (`Dockerfile` now installs `git`), not a
reopening of `#10`'s or `#11`'s already-passed gates — this ticket's own
blast radius (the `Dockerfile`) is exactly where the fix belongs.

## Live proof (2026-08-18, `docker build` + `docker run --read-only`)

```
$ docker build -t harness-doctrine .            # succeeds, git now installed
$ docker run -d --read-only -p 5050:5050 -p 5051:5051 \
    -v $(pwd):/harness:ro -e HARNESS_ROOT=/harness harness-doctrine
$ curl -s localhost:5050/api/health              -> 200                     (GH-31.2)
$ curl -s localhost:5050/api/doctrine/harness-v0.2/manifest
    -> real manifest JSON, git_commit populated (was ManifestBuildError pre-fix — #10's route, first time proven in Docker)
$ curl (no auth) .../mcp -d '{"method":"tools/list"}'           -> 401     (GH-31.5, fail-closed)
$ curl (Bearer token) .../mcp -d '{"method":"initialize"}'      -> 200, session established
$ curl (same session) .../mcp -d '{"method":"tools/list"}'
    -> [harness_get_template, harness_get_gate, harness_get_standard, harness_search_doctrine]
$ curl (same session) .../mcp tools/call harness_get_template   -> real content + {version,path,sha256} provenance  (GH-31.5, matches #11's bare-process demo exactly)
$ docker exec ... python3 -c "os.kill(<mcp-pid>, SIGTERM)"
    -> entrypoint log: "container-entrypoint: mcp process exited (code 143) -- browser keeps running"
    -> browser /api/health still 200 after mcp killed                       (GH-31.6)
    -> HEALTHCHECK next poll: exit 1, "unhealthy: mcp: [Errno 111] Connection refused" -- names which process failed (GH-31.3)
    -> container itself stayed up (RestartCount=0, Status=running) -- one process dying didn't tear down the other
$ docker exec harness-test id
    -> uid=10001(harness) gid=999(harness)                                  (GH-31.7)
$ docker logs harness-test | grep -i "read-only|permission denied"
    -> no matches -- no filesystem-write failures under --read-only          (GH-31.4)
```

All 7 acceptance criteria verified live, not asserted. `scripts/verify.sh` also reproduced green (73 tests, 94% cov, no application code changed).

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `Dockerfile`; two new small scripts (`scripts/container-entrypoint.sh`, `scripts/container-healthcheck.py`) — no application code, no new MCP tool/HTTP route, no contract change |
| Known consumers | none yet — `#11` has never been run through Docker by anyone; this is additive |
| Data elements | none |
| Deploy surface | container image only — this is exactly the deploy surface, that's the point of the ticket |

## Rollback note

Revert the commit — `Dockerfile` returns to browser-only, the two new scripts are simply unused/removed. No migration, no config a consumer depends on (none exist yet).

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same MCP/HTTP contracts `#10`/`#11` already shipped and G6-cleared; this only changes how the existing process is launched | G2 |
| Decision that deviates from the existing pattern? | No — topology (same container, second process, separate port) was already decided by `#11`'s own ticket body, not invented here. The process-supervision shape (bash `trap`/`wait -n`, no new init system) is the smallest addition that satisfies the requirement, consistent with this repo's existing "keep the image minimal" pattern (`Dockerfile`'s comments already justify every line added) | ADR |
| Effort beyond ~3 days after recon? | No — hours, reusing `#9`'s already-proven read-only/non-root posture directly | G1 |
| Tier raised during recon? | No — stays T2 | re-approve |

## GC sign-off

T2: Driver. **Approved in-session, 2026-08-18** (not via issue #31 comment — ADR-012's synchronous carve-out: Driver actively present in a live session and chose to render the verdict there; noted on [issue #31](https://github.com/JanusCoetzee/AI_WF_Harness/issues/31#issuecomment-5324195471) for the record). `DECISIONS.log`: `2026-08-18 | GC passed | janus | GH-31`
