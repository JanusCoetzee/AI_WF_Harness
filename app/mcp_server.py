"""#11 — MCP tools serving doctrine content over `streamable-http`, with
provenance and fail-closed authz (ADR-002's MCP tool table; transport
resolved to HTTP-only 2026-08-18 — stdio has no per-request identity, see
`#11`'s ticket body).

Reuses `#10`'s content-store and authz module **directly** — same
in-process `app/doctrine.py` calls `app/server.py`'s HTTP routes make, no
HTTP hop between this process and that module. The two processes share a
container but not a request path.

Design: the four tools' actual logic lives in plain, synchronous functions
(`_get_by_kind`, `_search`) that take `identity` as an explicit argument —
testable without spinning up the MCP protocol machinery at all. The
`@mcp.tool()`-decorated wrappers are thin: pull identity via
`get_access_token()`, delegate, translate `doctrine.py`'s exceptions into
`ToolError` (never let a raw exception cross the tool boundary — the
whole point of "tool error, not content" per every one of #11's ACs).
"""
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.provider import AccessToken, TokenVerifier
from mcp.server.auth.settings import AuthSettings
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

try:  # package import (pytest from repo root)
    from app import doctrine
    from app.server import ROOT, catalog
except ImportError:  # script run: app/ on sys.path
    import doctrine
    from server import ROOT, catalog

# ADR-002's four tools map 1:1 onto three of build_manifest()'s `kind`
# values; "doc"/"stage" have no dedicated fetch tool (unchanged scope from
# the original G2 design — search is the only route to them).
_KIND_BY_TOOL = {"template": "template", "gate": "gate", "standard": "standard"}


class StubTokenVerifier(TokenVerifier):
    """v1 identity stub mirroring #10's `X-Harness-Actor` header stub
    exactly: presence of any non-empty bearer token = authenticated, no
    real OIDC yet. Real SSO/OIDC is a G7 deployment blocker (#10's
    threat-model delta), not something #11 is expected to solve."""

    async def verify_token(self, token: str) -> AccessToken | None:
        if not token or not token.strip():
            return None
        return AccessToken(token=token, client_id=token, scopes=[])


def _identity_from_access_token() -> dict:
    token = get_access_token()
    return {"authenticated": token is not None, "roles": []}


def _resolve_manifest_or_error(version: str) -> dict:
    try:
        return doctrine.build_manifest(ROOT, version, catalog())
    except KeyError as exc:
        raise ToolError(f"unknown doctrine version: {version}") from exc
    except doctrine.ManifestBuildError as exc:
        raise ToolError(f"doctrine manifest could not be built: {exc}") from exc


def _get_by_kind(kind: str, name: str, version: str, identity: dict) -> dict:
    manifest = _resolve_manifest_or_error(version)
    entry = next(
        (f for f in manifest["files"]
         if f["kind"] == kind and Path(f["path"]).stem.lower() == name.lower()),
        None,
    )
    if entry is None:
        raise ToolError(f"no {kind} named {name!r} at {version}")
    if not doctrine.is_allowed(identity, entry):
        raise ToolError(f"not authorized to read {entry['path']}")
    try:
        return doctrine.read_file_verified(ROOT, manifest, entry["path"])
    except doctrine.IntegrityError as exc:
        raise ToolError(f"integrity check failed for {entry['path']}") from exc


def _search(query: str, version: str, identity: dict) -> list[dict]:
    manifest = _resolve_manifest_or_error(version)
    q = query.strip().lower()
    hits = []
    for f in manifest["files"]:
        if not doctrine.is_allowed(identity, f):
            continue  # fail-closed: denied items never appear in results either
        if q in f["title"].lower() or q in f["path"].lower():
            hits.append({"path": f["path"], "title": f["title"], "excerpt": f["title"]})
    return hits


# --- SDK server + tool registration -----------------------------------

# Not a real OAuth issuer — the SDK's metadata routes require these URLs
# even though StubTokenVerifier makes the actual trust decision (bearer-
# token presence only). Overridable for real deployment; localhost
# defaults are fine for local dev / tests, same pattern as #9's
# HARNESS_ROOT env var.
ISSUER_URL = os.environ.get("HARNESS_MCP_ISSUER_URL", "http://localhost:5050/stub-issuer")
RESOURCE_SERVER_URL = os.environ.get("HARNESS_MCP_RESOURCE_URL", "http://localhost:5051/mcp")

mcp = MCPServer(
    "harness-doctrine",
    token_verifier=StubTokenVerifier(),
    auth=AuthSettings(issuer_url=ISSUER_URL, resource_server_url=RESOURCE_SERVER_URL),
)


@mcp.tool()
def harness_get_template(name: str, version: str) -> dict:
    """Fetch a CHANGE/PRD/ADR/... template by name at an explicit doctrine
    version. Returns {path, version, sha256, content}."""
    return _get_by_kind("template", name, version, _identity_from_access_token())


@mcp.tool()
def harness_get_gate(gate: str, version: str) -> dict:
    """Fetch a gate's evidence requirements by name (e.g. "G4") at an
    explicit doctrine version. Returns {path, version, sha256, content}."""
    return _get_by_kind("gate", gate, version, _identity_from_access_token())


@mcp.tool()
def harness_get_standard(std_id: str, version: str) -> dict:
    """Fetch STANDARDS.md's text at an explicit doctrine version. Returns
    {path, version, sha256, content}. (There is one STANDARDS.md, not one
    file per STD-### — `std_id` is accepted for ADR-002's contract shape
    but the whole document is returned; callers grep their STD-### in it.)"""
    return _get_by_kind("standard", "STANDARDS", version, _identity_from_access_token())


@mcp.tool()
def harness_search_doctrine(query: str, version: str) -> list[dict]:
    """Ranked title/path match over the manifest's files[] at an explicit
    doctrine version (skills[] is a composition pin, not searchable
    content — out of scope, see #11). Returns [{path, title, excerpt}]."""
    return _search(query, version, _identity_from_access_token())


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host=os.environ.get("MCP_HOST", "127.0.0.1"),
        port=int(os.environ.get("MCP_PORT", "5051")),
    )
