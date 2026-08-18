# RECON — #31 (containerize #11's MCP process alongside #9's browser)

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Current container entrypoint | `Dockerfile:22` | `CMD ["sh", "-c", "exec gunicorn ... app.server:app"]` — browser only |
| Current health check | `Dockerfile:19-20` | Polls `http://127.0.0.1:5050/api/health` (Flask route, `app/server.py:223`) — no equivalent exists for MCP |
| MCP process entrypoint | `app/mcp_server.py:145-151` | `mcp.run(transport="streamable-http", host=MCP_HOST, port=MCP_PORT)` — `MCP_HOST` defaults `127.0.0.1` (wrong for container reachability, needs `0.0.0.0`), `MCP_PORT` defaults `5051` |
| MCP run() internals | `.venv/…/mcp/server/mcpserver.py` (installed dependency) | `anyio.run(self.run_streamable_http_async(**kwargs))` — synchronous, blocking, own event loop — same shape as `gunicorn`'s blocking foreground process, cannot share a WSGI worker |
| Existing non-root/read-only posture | `Dockerfile:14-16, 24` | `useradd --system --uid 10001 harness` before `USER harness`; gunicorn's `--worker-tmp-dir /dev/shm` is the one filesystem-write accommodation already made for `--read-only` |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| Local dev / CI | `docker build`/`docker run` isn't in `verify.sh` or CI (`grep -rn docker scripts/ .github/` — no hits) — this ticket's proof is manual, same as `#9`'s and `#11`'s own G4 evidence | grep |
| `#11`'s own demo record | `PLAN.md`'s M2 demo runs `mcp_server.py` bare, not containerized — this ticket's AC #5 explicitly re-runs that same sequence against the container instead | `PLAN.md` |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| Container exposes exactly one service (`5050`) | `Dockerfile` as it stands | Changing — this ticket adds a second exposed port (`5051`). No consumer currently depends on the container being single-service (nothing calls it that way yet; `#11` was never run through Docker at all) |
| `gunicorn`'s crash takes the whole container down (single `CMD`, single foreground process = container's lifecycle) | Current `Dockerfile` shape | Changing deliberately — two independent foreground processes means one dying no longer has to mean the container's lifecycle ends. Named explicitly in the Decision section below since it's a real behavior change, not incidental |

## Test coverage reality

No existing test drives the container itself (bash/Docker, outside `pytest`'s scope, consistent with `#9`'s own precedent — its G4 evidence was also a live manual `docker run`, not an automated test). This ticket adds no new `pytest` coverage; its evidence is a live, reproduced `docker build && docker run` sequence with `#11`'s own MCP demo re-run against the containerized endpoint — same rigor `#9` was held to, pasted into this ticket's evidence section, not just asserted.

## Real constraint found during recon — narrows one acceptance criterion, named not silently reinterpreted

`#31`'s own AC #6 (filed before this recon) asked for "the container's own health status reflects only the process that actually failed." **Docker's `HEALTHCHECK` is a single pass/fail bit per container** — there is no mechanism for a container to report two independent health states to `docker ps`/an orchestrator. What *is* achievable, and what this change actually delivers:

- The health-check script polls both processes and prints which one failed to its own stdout (visible via `docker inspect --format='{{json .State.Health}}'` and `docker logs`) — diagnosable, not silent, but still a single healthy/unhealthy bit at the container level.
- Killing one process does **not** crash or exit the other (achieved at the process-supervision level, in the entrypoint script, independent of the health-check bit) — the surviving process keeps actually serving traffic even while the container reports unhealthy.
- This mirrors a decision this repo already made and defended: `THREAT-MODEL.md`'s control-failure-semantics table treats "service availability" as **"open — by design"**, and ADR-008's registry-boundary consequence explicitly separates *availability* from *correctness*. A single-bit container health signal, with an orchestrator (ECS, in the real deploy) restarting the whole task on unhealthy, is consistent with that existing posture, not a new one invented for this ticket.

**Not a hedge, not a silent reinterpretation:** flagged here, and AC #6 in `CHANGE.md` is written to match what's actually achievable rather than an unrealistic two-independent-signals design Docker itself doesn't support.

## Go / No-go

- [x] Blast radius confirmed (Dockerfile + two small new scripts, no application code/contract changes)
- [x] No consumer contract broken (nothing outside this repo drives the container yet)
- [x] `mcp` package internals checked directly (not assumed) — no filesystem writes in `mcp/server/`, so no `/dev/shm`-style accommodation is expected to be needed for the MCP process specifically; verified live below anyway, not just by source inspection
- **Recommendation:** go
