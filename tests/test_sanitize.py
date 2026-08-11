"""GH-14 / ADR-009: rendered markdown must be sanitized before `| safe`.

Written red-first against the pre-fix code (page.html's `{{ body | safe }}`
over raw markdown() output) — GH-14.1 failed before the fix, passes after.
GH-14.2 pins that the allowlist still covers every construct real docs use.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from server import MD_EXTENSIONS, _sanitize, app, md_render  # noqa: E402


def render(md_source: str) -> str:
    return _sanitize(md_render(md_source, extensions=MD_EXTENSIONS))


def test_script_tag_is_stripped():
    """GH-14.1"""
    out = render("hello <script>alert(1)</script> world")
    assert "<script" not in out
    assert "alert(1)" not in out or "<script>" not in out  # text may remain, tag must not


def test_event_handler_attribute_is_stripped():
    """GH-14.1"""
    out = render('<img src=x onerror="alert(1)">')
    assert "onerror" not in out


def test_javascript_href_is_stripped():
    """GH-14.1"""
    out = render("[click me](javascript:alert(1))")
    assert "javascript:" not in out


def test_legitimate_constructs_survive_sanitization():
    """GH-14.2 — every tag MD_EXTENSIONS + base markdown produce in this repo's
    own docs must still render after sanitization."""
    out = render(
        "# Title\n\n"
        "Some *em* and **strong** and `code`.\n\n"
        "- a\n- b\n\n"
        "| A | B |\n|---|---|\n| 1 | 2 |\n\n"
        "```python\nprint(1)\n```\n\n"
        "> quote\n\n"
        "[link](http://example.com)\n"
    )
    for tag in ("<h1>", "<em>", "<strong>", "<code>", "<ul>", "<li>",
                "<table>", "<th>", "<td>", "<pre>", "<blockquote>", "<a href="):
        assert tag in out, f"{tag} missing from sanitized output"


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_real_doc_pages_still_render_after_sanitization(client):
    """GH-14.2 — full route, not just the helper: existing repo docs unaffected."""
    r = client.get("/s/gates/gates")
    assert r.status_code == 200
    assert "<table>" in r.get_data(as_text=True)
