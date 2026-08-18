"""#11 — MCP tools. Acceptance criteria 1-5 (ticket body). Tests the plain
functions (`_get_by_kind`, `_search`) directly rather than driving the MCP
protocol over a real transport — those functions are exactly what the
`@mcp.tool()` wrappers delegate to, and this keeps the suite fast and
independent of network/ASGI plumbing. Tool *registration* (AC3) is
checked once against the real `mcp.list_tools()`, so the wiring itself
isn't left untested."""
import asyncio
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
import doctrine  # noqa: E402
import mcp_server as srv  # noqa: E402
from mcp.server.mcpserver.exceptions import ToolError  # noqa: E402

VERSION = "harness-v0.2"
AUTHED = {"authenticated": True, "roles": []}
ANON = {"authenticated": False, "roles": []}


# --- AC 3: exactly the four ADR-002 tools, none mutates state, no stdio ---

def test_11_3_exactly_four_tools_registered():
    tools = asyncio.run(srv.mcp.list_tools())
    names = {t.name for t in tools}
    assert names == {
        "harness_get_template", "harness_get_gate",
        "harness_get_standard", "harness_search_doctrine",
    }


def test_11_3_no_write_tool_exists():
    tools = asyncio.run(srv.mcp.list_tools())
    for t in tools:
        # ADR-002: every tool is read-only by contract. No mechanical
        # "readOnlyHint" is guaranteed set by every SDK version, so the
        # real assertion is the tool list itself never grows a write verb.
        assert not any(verb in t.name for verb in ("set_", "write_", "delete_", "create_"))


# --- AC 1: successful fetch carries {version, path, sha256} provenance ---

def test_11_1_get_template_returns_content_with_provenance():
    result = srv._get_by_kind("template", "CHANGE", VERSION, AUTHED)
    assert set(result) == {"path", "version", "sha256", "content"}
    assert result["version"] == VERSION
    assert result["path"] == "templates/CHANGE.md"
    assert len(result["sha256"]) == 64
    assert result["content"]


def test_11_1_get_gate_and_standard_also_return_provenance():
    gate = srv._get_by_kind("gate", "GATES", VERSION, AUTHED)
    assert gate["path"] == "gates/GATES.md"
    std = srv._get_by_kind("standard", "STANDARDS", VERSION, AUTHED)
    assert std["path"] == "docs/STANDARDS.md"


# --- AC 2: unknown version -> tool error, never silent fallback ----------

def test_11_2_unknown_version_raises_tool_error():
    with pytest.raises(ToolError, match="unknown doctrine version"):
        srv._get_by_kind("template", "CHANGE", "harness-v99.9", AUTHED)


def test_11_2_unknown_item_name_raises_tool_error():
    with pytest.raises(ToolError, match="no template named"):
        srv._get_by_kind("template", "DOES-NOT-EXIST", VERSION, AUTHED)


# --- AC 4: denied item -> denial tool error, content never returned ------

def test_11_4_unauthenticated_identity_denied():
    with pytest.raises(ToolError, match="not authorized"):
        srv._get_by_kind("template", "CHANGE", VERSION, ANON)


def test_11_4_search_silently_omits_denied_items_not_erroring():
    # Denial in search context means "not in the result set", not a thrown
    # error (there's no single item being fetched) -- still fail-closed.
    authed_hits = srv._search("CHANGE", VERSION, AUTHED)
    anon_hits = srv._search("CHANGE", VERSION, ANON)
    assert len(authed_hits) > 0
    assert anon_hits == []


# --- AC 5: tamper -> integrity tool error, content never returned --------

def test_11_5_tampered_item_raises_tool_error_not_content(monkeypatch):
    real_manifest = doctrine.build_manifest(srv.ROOT, VERSION, srv.catalog())
    corrupted = {
        **real_manifest,
        "files": [
            {**f, "sha256": "0" * 64} if f["path"] == "templates/CHANGE.md" else f
            for f in real_manifest["files"]
        ],
    }
    monkeypatch.setattr(srv, "_resolve_manifest_or_error", lambda v: corrupted)

    with pytest.raises(ToolError, match="integrity check failed"):
        srv._get_by_kind("template", "CHANGE", VERSION, AUTHED)


# --- StubTokenVerifier: bearer-token presence gates identity -------------

def test_stub_token_verifier_accepts_nonempty_token():
    token = asyncio.run(srv.StubTokenVerifier().verify_token("some-bearer-token"))
    assert token is not None
    assert token.client_id == "some-bearer-token"


def test_stub_token_verifier_rejects_empty_token():
    assert asyncio.run(srv.StubTokenVerifier().verify_token("")) is None
    assert asyncio.run(srv.StubTokenVerifier().verify_token("   ")) is None


# --- Registered @mcp.tool() wrappers, not just the pure functions --------
# call_tool() drives the actual registered tool (real parameter names,
# real delegation) -- proves the wiring, not only the logic underneath it.
# No live auth context exists here, so get_access_token() returns None
# (unauthenticated) same as the ANON fixture above; that's still a real,
# useful assertion (correct parameter wiring end to end), just not the
# authenticated-happy-path shape covered by the pure-function tests.

def test_11_wrapper_get_gate_propagates_unknown_item_error():
    with pytest.raises(ToolError, match="no gate named"):
        asyncio.run(srv.mcp.call_tool(
            "harness_get_gate", {"gate": "DOES-NOT-EXIST", "version": VERSION}
        ))


def test_11_wrapper_get_standard_wiring():
    with pytest.raises(ToolError, match="not authorized"):
        # unauthenticated (no live auth context) -> denied, same fail-closed
        # path as test_11_4_unauthenticated_identity_denied, reached this
        # time through the real registered tool, not the pure function
        asyncio.run(srv.mcp.call_tool(
            "harness_get_standard", {"std_id": "STD-001", "version": VERSION}
        ))


def test_11_wrapper_search_doctrine_returns_empty_when_unauthenticated():
    result = asyncio.run(srv.mcp.call_tool(
        "harness_search_doctrine", {"query": "CHANGE", "version": VERSION}
    ))
    assert result.is_error is False
    assert result.structured_content == {"result": []}
