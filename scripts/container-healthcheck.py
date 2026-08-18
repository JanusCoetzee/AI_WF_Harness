#!/usr/bin/env python3
"""Container HEALTHCHECK for the harness image (#31): checks both the
browser (HTTP GET /api/health) and the MCP process (TCP connect on its
port — a real protocol handshake needs a JSON-RPC/session dance that isn't
worth the complexity here; "is something actually listening" is the honest
bar for this check, same spirit as the browser's own liveness probe).

Docker's HEALTHCHECK is a single pass/fail bit per container (RECON.md,
GH-31) -- this script's job is to make failures diagnosable via `docker
logs`/`docker inspect`, not to report two independent signals Docker
itself has no way to surface.
"""
import socket
import sys
import urllib.request

BROWSER_URL = "http://127.0.0.1:5050/api/health"
MCP_HOST, MCP_PORT = "127.0.0.1", 5051
TIMEOUT = 2

failures = []

try:
    with urllib.request.urlopen(BROWSER_URL, timeout=TIMEOUT) as resp:
        if resp.status != 200:
            failures.append(f"browser: unexpected status {resp.status}")
except Exception as exc:  # noqa: BLE001 - health check, report anything
    failures.append(f"browser: {exc}")

try:
    socket.create_connection((MCP_HOST, MCP_PORT), timeout=TIMEOUT).close()
except Exception as exc:  # noqa: BLE001
    failures.append(f"mcp: {exc}")

if failures:
    print("unhealthy: " + "; ".join(failures))
    sys.exit(1)

print("healthy: browser + mcp both up")
sys.exit(0)
