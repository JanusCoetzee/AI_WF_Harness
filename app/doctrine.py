"""Doctrine content-store + authz (#10, ADR-002 read-side contracts, ADR-008
composition pin). Read-only: sha256-verified reads, explicit-version-only
manifests, fail-closed authz at the retrieval boundary.

No route/Flask code here on purpose — this module is the thing
`scripts/doctrine-manifest.py` and `app/server.py` both call, and the thing
`tests/test_doctrine_api.py` exercises directly without spinning up a client.
"""
from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import yaml

VERSION_PATTERN = r"^harness-v[0-9]+\.[0-9]+$"

# Maps app.server.catalog()'s section keys to ADR-002's manifest `kind` enum.
# "skills" is deliberately absent: skill composition is reported separately,
# in skills[] sourced from the config pin (ADR-008) — not scanned from disk
# here, so a skill file's presence/absence never silently changes the pin.
_SECTION_KIND = {
    "overview": "doc",
    "docs": "doc",
    "stages": "stage",
    "gates": "gate",
    "templates": "template",
    "evals": "doc",
    "config": "doc",
}

# v1 policy (ADR-002 amendment): current doctrine is uniformly Internal:
# no per-item differentiation exists yet (GH-21's publish-time classification
# gate — the thing that would actually assign finer labels — is out of scope
# for this ticket). The label is still carried explicitly on every item, so
# is_allowed()'s fail-closed check has something real to check rather than
# being vacuously true.
DEFAULT_CLASSIFICATION = "Internal"
KNOWN_CLASSIFICATIONS = ("Public", "Internal", "Confidential", "Restricted")

# v1 authz policy: any authenticated identity may read any item carrying a
# recognized classification label — no role required at any level yet.
# Tightening this to real per-level roles is a policy change (edit this
# dict / pass a different `policy`), not an architecture change.
ALLOW_ALL_AUTHENTICATED = {c: [] for c in KNOWN_CLASSIFICATIONS}


class IntegrityError(Exception):
    """On-disk bytes don't match the manifest's recorded sha256. Callers
    must turn this into a 500, never serve the content (ADR-002 fail-closed
    integrity contract)."""


class ManifestBuildError(Exception):
    """The manifest couldn't be built at all — e.g. HARNESS_ROOT has no
    `.git` (found by G5 adversarial review: a content root delivered as a
    stripped bundle rather than a live checkout, or a minimal image with no
    `git` binary, both plausible under ADR-008's published-tag model).
    Callers must turn this into a clean 500, not let the underlying
    CalledProcessError propagate as an unhandled exception."""


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_commit(root: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise ManifestBuildError(
            f"could not resolve git_commit for {root}: {exc}"
        ) from exc
    return out.stdout.strip()


def _load_pin(root: Path) -> dict:
    cfg = yaml.safe_load((root / "harness.config.yaml").read_text(encoding="utf-8"))
    pin = (cfg or {}).get("doctrine")
    if not pin:
        raise ValueError("harness.config.yaml has no `doctrine:` composition pin")
    return pin


def build_manifest(root: Path, version: str, catalog: list[dict]) -> dict:
    """Build the manifest for `version`. `catalog` is app.server.catalog()'s
    output, passed in rather than imported to avoid a server->doctrine->
    server import cycle and to keep this module Flask-free."""
    pin = _load_pin(root)
    if version != pin["version"]:
        raise KeyError(f"unknown doctrine version: {version}")

    files = []
    for section in catalog:
        kind = _SECTION_KIND.get(section["key"])
        if kind is None:  # "skills" section — reported via skills[] instead
            continue
        for item in section["items"]:
            path = root / item["path"]
            entry_kind = "standard" if item["path"] == "docs/STANDARDS.md" else kind
            files.append({
                "path": item["path"],
                "sha256": sha256_of(path),
                "kind": entry_kind,
                "title": item["title"],
                "classification": DEFAULT_CLASSIFICATION,
            })

    return {
        "version": version,
        "git_commit": _git_commit(root),
        "files": files,
        "skills": list(pin.get("skills", [])),
    }


def read_file_verified(root: Path, manifest: dict, rel_path: str) -> dict:
    """Return `{path, version, sha256, content}` for a path listed in
    `manifest`. Raises KeyError if the path isn't in the manifest (caller:
    404), IntegrityError if on-disk bytes don't match the recorded hash
    (caller: 500, never the content)."""
    entry = next((f for f in manifest["files"] if f["path"] == rel_path), None)
    if entry is None:
        raise KeyError(rel_path)

    disk_path = root / rel_path
    actual_sha256 = sha256_of(disk_path)
    if actual_sha256 != entry["sha256"]:
        raise IntegrityError(
            f"{rel_path}: manifest sha256 {entry['sha256']} != on-disk {actual_sha256}"
        )

    return {
        "path": rel_path,
        "version": manifest["version"],
        "sha256": actual_sha256,
        "content": disk_path.read_text(encoding="utf-8"),
    }


def is_allowed(identity: dict | None, item: dict, policy: dict | None = None) -> bool:
    """Fail-closed authz at the retrieval boundary (ADR-002 RBAC amendment:
    "RBAC is enforced at the retrieval boundary, never inside the model").

    An item with a missing or unrecognized classification label is denied
    regardless of identity or policy — labeling is a publish-time
    responsibility (GH-21), this boundary never invents a label on read.
    """
    classification = item.get("classification")
    if classification not in KNOWN_CLASSIFICATIONS:
        return False
    if not identity or not identity.get("authenticated"):
        return False

    allowed_roles = (policy or ALLOW_ALL_AUTHENTICATED).get(classification)
    if allowed_roles is None:
        return False
    if not allowed_roles:  # empty list == authentication alone is sufficient
        return True
    return bool(set(identity.get("roles", [])) & set(allowed_roles))
