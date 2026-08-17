#!/usr/bin/env python3
"""Build and print the doctrine manifest, standalone (no Flask server
needed) — runnable in CI to catch a broken/tampered manifest before deploy.

Usage: scripts/doctrine-manifest.py [version]
  version defaults to harness.config.yaml's doctrine.version pin.
Exit non-zero (and prints to stderr) on an unknown version or any file the
manifest would build with unreadable/inconsistent content.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app import doctrine  # noqa: E402
from app.server import catalog  # noqa: E402


def main() -> int:
    pin = doctrine._load_pin(ROOT)
    version = sys.argv[1] if len(sys.argv) > 1 else pin["version"]
    try:
        manifest = doctrine.build_manifest(ROOT, version, catalog())
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
