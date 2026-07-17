"""GH-6: the eval suite is browsable in the harness browser."""
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


def test_catalog_has_evals_section(client):
    """GH-6.1"""
    data = client.get("/api/catalog").get_json()
    evals = next((s for s in data if s["key"] == "evals"), None)
    assert evals is not None
    slugs = {i["slug"] for i in evals["items"]}
    assert "report" in slugs and "manifest" in slugs
    assert any(s.startswith("gt-") for s in slugs), "ground truths listed"
    assert any("payment-triage" in s for s in slugs), "scenario briefs listed"


def test_eval_pages_render(client):
    """GH-6.2 — markdown and raw-YAML paths both 200."""
    assert client.get("/s/evals/report").status_code == 200
    r = client.get("/s/evals/gt-greenfield")
    assert r.status_code == 200
    assert "class='raw'" in r.get_data(as_text=True)
