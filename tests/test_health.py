"""CHG-001: /api/health endpoint and home-page counts."""
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


def test_health_returns_ok_with_counts(client):
    """CHG-001.1"""
    r = client.get("/api/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] == "ok"
    assert data["documents"] > 0
    assert data["skills"] > 0


def test_health_counts_match_catalog(client):
    """CHG-001.1 — counts derive from the same catalog the UI serves."""
    health = client.get("/api/health").get_json()
    sections = client.get("/api/catalog").get_json()
    docs = sum(len(s["items"]) for s in sections if s["key"] != "skills")
    skills = sum(len(s["items"]) for s in sections if s["key"] == "skills")
    assert health["documents"] == docs
    assert health["skills"] == skills


def test_home_hero_shows_counts(client):
    """CHG-001.2"""
    health = client.get("/api/health").get_json()
    html = client.get("/").get_data(as_text=True)
    assert f"{health['documents']} documents" in html
    assert f"{health['skills']} skills" in html
