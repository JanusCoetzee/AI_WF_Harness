#!/usr/bin/env bash
# Container entrypoint (#31): launches both harness processes -- the
# browser (gunicorn/app.server:app, WSGI) and the MCP endpoint
# (app/mcp_server.py, its own blocking event loop via mcp.run()) -- as
# independent foreground children of this script, not two apps crammed
# into one process model (they can't be; see RECON.md).
#
# Deliberately does NOT kill the survivor when one child dies (GH-31.6):
# the surviving process keeps serving real traffic even while the
# container's own HEALTHCHECK bit goes unhealthy -- consistent with this
# repo's existing "availability is open by design" posture
# (THREAT-MODEL.md's control-failure-semantics table), not a new one
# invented here. An orchestrator restarting the whole container on
# unhealthy is the expected recovery path, same as any single-process
# container's crash-restart today.
set -uo pipefail

on_term() {
  echo "container-entrypoint: forwarding TERM to children" >&2
  kill -TERM "${GUNICORN_PID:-}" "${MCP_PID:-}" 2>/dev/null || true
}
trap on_term TERM INT

gunicorn --bind "0.0.0.0:${PORT:-5050}" --workers 2 --worker-tmp-dir /dev/shm app.server:app &
GUNICORN_PID=$!

python app/mcp_server.py &
MCP_PID=$!

# Wait for the first child to exit, log it, then keep waiting for whichever
# is still running -- one dying does not tear down the other.
wait -n "$GUNICORN_PID" "$MCP_PID"
FIRST_EXIT=$?
if ! kill -0 "$GUNICORN_PID" 2>/dev/null; then
  echo "container-entrypoint: browser process exited (code $FIRST_EXIT) -- mcp keeps running" >&2
elif ! kill -0 "$MCP_PID" 2>/dev/null; then
  echo "container-entrypoint: mcp process exited (code $FIRST_EXIT) -- browser keeps running" >&2
fi

wait
