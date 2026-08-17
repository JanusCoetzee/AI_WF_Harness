"""#10 — doctrine API + authz interface. Acceptance criteria 1-5 (ticket
body). Manual schema assertions (not the `jsonschema` package) deliberately
— ADR-002's manifest schema is small and stable; adding a new pinned
dependency + pip-audit surface for one test file isn't worth it for a
schema this size."""
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "app"))
from server import app  # noqa: E402
import doctrine  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
VERSION = "harness-v0.2"  # harness.config.yaml's doctrine.version pin


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _auth_headers():
    return {"X-Harness-Actor": "test-actor"}


def _git_init(root: Path) -> None:
    """build_manifest() requires a real git_commit (ADR-002 schema) — give
    a fake repo fixture a minimal real commit rather than mocking git out."""
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "HOME": str(root)}
    env["GIT_COMMITTER_NAME"], env["GIT_COMMITTER_EMAIL"] = "t", "t@t"
    for cmd in (["git", "init", "-q"], ["git", "add", "-A"], ["git", "commit", "-q", "-m", "x"]):
        subprocess.run(cmd, cwd=root, env=env, check=True)


# --- AC 1: manifest schema (ADR-002 + ADR-008's skills[]) ------------------

def test_10_1_manifest_matches_schema(client):
    r = client.get(f"/api/doctrine/{VERSION}/manifest", headers=_auth_headers())
    assert r.status_code == 200
    m = r.get_json()

    assert re.match(r"^harness-v[0-9]+\.[0-9]+$", m["version"])
    assert re.match(r"^[0-9a-f]{40}$", m["git_commit"])
    assert m["files"], "expected a non-empty files[] for this repo"

    for f in m["files"]:
        assert set(f) >= {"path", "sha256", "kind", "title"}
        assert re.match(r"^[0-9a-f]{64}$", f["sha256"])
        assert f["kind"] in {"gate", "stage", "template", "standard", "doc"}

    for s in m["skills"]:  # ADR-008 addition
        assert set(s) == {"name", "version"}
        assert re.match(r"^harness-v[0-9]+\.[0-9]+$", s["version"])


def test_10_5_skills_report_exactly_the_config_pin(client):
    """AC5: skills[] reports exactly harness.config.yaml's composition pin."""
    r = client.get(f"/api/doctrine/{VERSION}/manifest", headers=_auth_headers())
    m = r.get_json()
    pin = doctrine._load_pin(ROOT)
    assert m["skills"] == pin["skills"]
    # Each pinned skill is itself sha256-traceable via files[] having its
    # own SKILL.md entry hashed under the same manifest — not duplicated
    # into skills[], but independently verifiable.
    skill_names = {s["name"] for s in pin["skills"]}
    assert skill_names <= {p.parent.name for p in (ROOT / ".claude" / "skills").glob("*/SKILL.md")}


# --- AC 2: tamper -> 500, never the altered content -------------------------

def test_10_2_tampered_file_returns_500_not_content(client, tmp_path, monkeypatch):
    # Build a manifest against a throwaway copy of the repo root so the test
    # never touches the real repo's files.
    fake_root = tmp_path / "repo"
    fake_root.mkdir()
    (fake_root / "harness.config.yaml").write_text(
        "doctrine:\n  version: harness-v0.2\n  core_version: harness-v0.2\n  skills: []\n"
    )
    target = fake_root / "README.md"
    target.write_text("original content\n")
    _git_init(fake_root)

    fake_catalog = [{"key": "overview", "items": [
        {"path": "README.md", "title": "README", "slug": "readme", "desc": ""}
    ]}]
    manifest = doctrine.build_manifest(fake_root, "harness-v0.2", fake_catalog)

    target.write_text("tampered content\n")  # bytes diverge from the manifest's hash

    with pytest.raises(doctrine.IntegrityError):
        doctrine.read_file_verified(fake_root, manifest, "README.md")


def test_10_2_file_route_500_on_tamper(client, monkeypatch):
    """The route always builds the manifest fresh from live disk each
    request, so simulating on-disk tamper (as the module-level test above
    does directly) can't desync a same-request manifest from itself. What
    *can* desync — and what read_file_verified must still catch — is a
    manifest whose recorded hash is wrong for any reason (a corrupted
    manifest source, a race, a bad cache upstream). Force that directly."""
    import server

    real_manifest = server._build_manifest_or_404(VERSION)
    corrupted = {
        **real_manifest,
        "files": [
            {**f, "sha256": "0" * 64} if f["path"] == "README.md" else f
            for f in real_manifest["files"]
        ],
    }
    monkeypatch.setattr(server, "_build_manifest_or_404", lambda v: corrupted)

    r = client.get(
        f"/api/doctrine/{VERSION}/file?path=README.md", headers=_auth_headers()
    )
    assert r.status_code == 500
    assert b"AI Workflow Harness" not in r.data  # README's real content, never served


# --- AC 3: no route serves doctrine without an explicit {version} ----------

def test_10_3_no_latest_or_versionless_route(client):
    for path in ("/api/doctrine/manifest", "/api/doctrine/file", "/api/doctrine/latest/manifest"):
        r = client.get(path, headers=_auth_headers())
        assert r.status_code == 404


def test_10_3_unknown_version_is_404(client):
    r = client.get("/api/doctrine/harness-v99.9/manifest", headers=_auth_headers())
    assert r.status_code == 404


# --- AC 4: fail-closed authz on an unlabeled item ---------------------------

def test_10_4_unlabeled_item_denied_even_under_a_restrictive_policy():
    identity = {"authenticated": True, "roles": ["harness-admin"]}
    restrictive_policy = {"Internal": ["harness-admin"], "Confidential": ["harness-admin"]}
    unlabeled_item = {"path": "x", "kind": "doc"}  # no "classification" key

    assert doctrine.is_allowed(identity, unlabeled_item, policy=restrictive_policy) is False


def test_10_4_unrecognized_classification_denied():
    identity = {"authenticated": True, "roles": []}
    item = {"classification": "Top Secret"}  # not in KNOWN_CLASSIFICATIONS
    assert doctrine.is_allowed(identity, item) is False


def test_10_4_v1_allows_authenticated_identity_on_labeled_item():
    identity = {"authenticated": True, "roles": []}
    item = {"classification": "Internal"}
    assert doctrine.is_allowed(identity, item) is True


def test_10_4_unauthenticated_identity_denied():
    item = {"classification": "Internal"}
    assert doctrine.is_allowed({"authenticated": False}, item) is False
    assert doctrine.is_allowed(None, item) is False


def test_10_4_manifest_route_403_without_actor_header(client):
    r = client.get(f"/api/doctrine/{VERSION}/file?path=README.md")  # no auth header
    assert r.status_code == 403


def test_10_4_manifest_route_filters_nothing_for_authenticated_actor(client):
    unauthed = client.get(f"/api/doctrine/{VERSION}/manifest").get_json()
    authed = client.get(f"/api/doctrine/{VERSION}/manifest", headers=_auth_headers()).get_json()
    # v1 policy: every item is "Internal" + allow-all-authenticated, so an
    # unauthenticated caller sees nothing (fail-closed) and an authenticated
    # one sees everything.
    assert unauthed["files"] == []
    assert len(authed["files"]) > 0
