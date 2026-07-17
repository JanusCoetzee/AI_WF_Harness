"""Characterization tests for CHG-001 (B1 recon).

Pin CURRENT behavior of the harness browser before changing it — including
behavior that merely *is*, not behavior that *should be*. A deliberate behavior
change must show up as a visible diff to one of these tests, never as a silent
side effect. (CHG-001.3)
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from server import app  # noqa: E402


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_home_returns_200_with_pipeline(client):
    r = client.get("/")
    assert r.status_code == 200
    html = r.get_data(as_text=True)
    assert 'class="chip stage"' in html
    assert 'class="chip gate"' in html


def test_catalog_sections_and_shape(client):
    r = client.get("/api/catalog")
    assert r.status_code == 200
    data = r.get_json()
    keys = [s["key"] for s in data]
    # GH-6 deliberately moved this pin: "evals" section added.
    assert keys == ["overview", "docs", "stages", "gates", "templates", "skills", "evals", "config"]
    first = data[0]["items"][0]
    assert set(first) == {"slug", "title", "path", "desc"}


def test_document_page_renders_markdown(client):
    r = client.get("/s/gates/gates")
    assert r.status_code == 200
    assert "<table>" in r.get_data(as_text=True)


def test_skill_page_shows_description(client):
    r = client.get("/s/skills/harness-status")
    assert r.status_code == 200
    assert "skill-desc" in r.get_data(as_text=True)


def test_config_page_renders_raw_yaml(client):
    r = client.get("/s/config/harness-config")
    assert r.status_code == 200
    assert "class='raw'" in r.get_data(as_text=True)


def test_unknown_paths_404(client):
    assert client.get("/s/nope/x").status_code == 404
    # CHG-001 deliberately un-pinned the previous 404 here: /api/health now exists.
    assert client.get("/api/health").status_code == 200
