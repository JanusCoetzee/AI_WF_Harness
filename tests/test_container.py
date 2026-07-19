"""#9 — containerized browser: content root comes from HARNESS_ROOT, falling
back to the repo the app lives in (criteria 1 and 3). The docker proof run
covers the rest of the ticket; these tests pin the root-resolution contract."""
from pathlib import Path

from app import server


def test_9_1_harness_root_env_overrides_content_root(monkeypatch, tmp_path):
    monkeypatch.setenv("HARNESS_ROOT", str(tmp_path))
    assert server._resolve_root() == tmp_path.resolve()


def test_9_3_default_root_is_own_repo_when_env_absent(monkeypatch):
    monkeypatch.delenv("HARNESS_ROOT", raising=False)
    repo_root = Path(server.__file__).resolve().parent.parent
    assert server._resolve_root() == repo_root


def test_9_3_module_root_matches_resolver_default():
    # The module-level ROOT (computed at import, without HARNESS_ROOT set in
    # the test env) must be the repo root — existing behavior pinned.
    repo_root = Path(server.__file__).resolve().parent.parent
    assert server.ROOT == repo_root
