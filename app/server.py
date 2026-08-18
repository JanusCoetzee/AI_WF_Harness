"""Harness Browser — serves the AI Workflow Harness (docs, stages, gates,
templates, skills, config) as a small web UI.

Run:  python3 app/server.py   →  http://localhost:5050
"""
from __future__ import annotations

import html
import os
import re
from pathlib import Path

import bleach
from flask import Flask, abort, jsonify, render_template, request
from markdown import markdown as md_render

try:  # package import (pytest from repo root, `from app import server`)
    from app import doctrine
except ImportError:  # script run: `python3 app/server.py` puts app/ on sys.path
    import doctrine


def _resolve_root() -> Path:
    """Content root: HARNESS_ROOT env (container: the read-only mount, #9),
    else the repo this app lives in (local dev, unchanged behavior)."""
    env = os.environ.get("HARNESS_ROOT")
    return Path(env).resolve() if env else Path(__file__).resolve().parent.parent


ROOT = _resolve_root()
MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

# GH-14 / ADR-009: python-markdown passes raw HTML in .md sources through
# unchanged, and page.html renders the result with `| safe`. Allowlist to
# exactly what MD_EXTENSIONS + base markdown legitimately produce (RECON.md
# confirmed this set against every doc in the repo) — anything else (script,
# iframe, event-handler attributes, ...) is stripped, not passed through.
SAFE_TAGS = [
    "p", "br", "hr", "em", "strong", "code", "pre",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "ul", "ol", "li",
    "table", "thead", "tbody", "tr", "th", "td",
    "blockquote", "a", "img",
]
SAFE_ATTRS = {
    "a": ["href", "title"],
    "img": ["src", "alt", "title"],
    "code": ["class"],  # fenced_code's "language-xxx" marker
}


def _sanitize(rendered_html: str) -> str:
    return bleach.clean(rendered_html, tags=SAFE_TAGS, attributes=SAFE_ATTRS, strip=True)

app = Flask(__name__)


def _title_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def _parse_skill(path: Path) -> tuple[str, str, str]:
    """Return (name, description, body) from a SKILL.md with YAML frontmatter."""
    text = path.read_text(encoding="utf-8")
    name, desc, body = path.parent.name, "", text
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if m:
        front, body = m.group(1), m.group(2)
        for line in front.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip()
    return name, desc, body


def _md_item(path: Path, slug: str | None = None, desc: str = "") -> dict:
    return {
        "slug": slug or path.stem.lower(),
        "title": _title_of(path),
        "path": str(path.relative_to(ROOT)),
        "desc": desc,
    }


def catalog() -> list[dict]:
    """Scan the repo fresh on every request — the harness is living documents."""
    sections: list[dict] = []

    def add(key: str, label: str, items: list[dict]) -> None:
        if items:
            sections.append({"key": key, "label": label, "items": items})

    overview = [p for p in (ROOT / "README.md", ROOT / "CLAUDE.md") if p.exists()]
    add("overview", "Overview", [_md_item(p) for p in overview])
    add("docs", "Philosophy & Operating Model",
        [_md_item(p) for p in sorted((ROOT / "docs").glob("*.md"))])
    add("stages", "Stages",
        [_md_item(p) for p in sorted((ROOT / "stages").glob("*.md"))])
    add("gates", "Gates",
        [_md_item(p) for p in sorted((ROOT / "gates").glob("*.md"))])
    add("templates", "Templates",
        [_md_item(p) for p in sorted((ROOT / "templates").glob("*.md"))])

    skills = []
    for p in sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        name, desc, _ = _parse_skill(p)
        skills.append({
            "slug": p.parent.name,
            "title": f"/{name}",
            "path": str(p.relative_to(ROOT)),
            "desc": desc,
        })
    add("skills", "Skills (slash commands)", skills)

    ev = ROOT / "evals" / "harness"
    if ev.is_dir():
        eval_items = []
        for name in ("README.md", "REPORT.md"):
            p = ev / name
            if p.exists():
                eval_items.append(_md_item(p, slug=p.stem.lower()))
        if (ev / "manifest.yaml").exists():
            eval_items.append({
                "slug": "manifest", "title": "manifest.yaml",
                "path": str((ev / "manifest.yaml").relative_to(ROOT)),
                "desc": "Pins each scenario's frozen ground truth to its accepted run",
            })
        eval_items += [_md_item(p) for p in sorted((ev / "scenarios").glob("*.md"))]
        for p in sorted((ev / "ground-truth").glob("*.yaml")):
            eval_items.append({
                "slug": f"gt-{p.stem}", "title": f"ground truth: {p.stem}",
                "path": str(p.relative_to(ROOT)),
                "desc": "Frozen before any run",
            })
        add("evals", "Evals (self-tests)", eval_items)

    cfg = ROOT / "harness.config.yaml"
    if cfg.exists():
        add("config", "Config", [{
            "slug": "harness-config",
            "title": "harness.config.yaml",
            "path": "harness.config.yaml",
            "desc": "Risk tiers, verify loop, fast-path policy, release policy",
        }])
    return sections


def _counts(sections: list[dict]) -> tuple[int, int]:
    """(documents, skills) — single source for UI and /api/health (CHG-001.2)."""
    docs = sum(len(s["items"]) for s in sections if s["key"] != "skills")
    skills = sum(len(s["items"]) for s in sections if s["key"] == "skills")
    return docs, skills


def _find(section_key: str, slug: str) -> tuple[dict, dict]:
    for section in catalog():
        if section["key"] == section_key:
            for item in section["items"]:
                if item["slug"] == slug:
                    return section, item
    abort(404)


# The pipeline map on the home page. (label, kind, section/slug link or None)
GREENFIELD = [
    ("IDEATE", "stage", "stages/00-ideation"), ("G0", "gate", "gates/gates"),
    ("DISCOVER", "stage", "stages/01-discovery"), ("G1", "gate", "gates/gates"),
    ("ARCHITECT", "stage", "stages/02-architecture"), ("G2", "gate", "gates/gates"),
    ("PLAN", "stage", "stages/03-planning"), ("G3", "gate", "gates/gates"),
    ("BUILD", "stage", "stages/04-implementation"), ("G4", "gate", "gates/gates"),
    ("REVIEW", "stage", "stages/05-review"), ("G5", "gate", "gates/gates"),
    ("SECURE", "stage", "stages/06-security-compliance"), ("G6", "gate", "gates/gates"),
    ("RELEASE", "stage", "stages/07-release-deployment"), ("G7", "gate", "gates/gates"),
    ("OPERATE", "stage", "stages/08-operate-learn"),
]
BROWNFIELD = [
    ("CHANGE INTAKE", "stage", "stages/b0-change-intake"),
    ("RECON", "stage", "stages/b1-reconnaissance"), ("GC", "gate", "gates/gates"),
    ("BUILD", "stage", "stages/04-implementation"), ("G4 →", "gate", "gates/gates"),
]


@app.route("/")
def index():
    sections = catalog()
    skills = next((s["items"] for s in sections if s["key"] == "skills"), [])
    doc_count, skill_count = _counts(sections)
    return render_template(
        "index.html", sections=sections, skills=skills,
        greenfield=GREENFIELD, brownfield=BROWNFIELD,
        doc_count=doc_count, skill_count=skill_count,
        active=None,
    )


@app.route("/s/<section_key>/<slug>")
def page(section_key: str, slug: str):
    section, item = _find(section_key, slug)
    path = ROOT / item["path"]
    if path.suffix in (".yaml", ".yml"):
        body = f"<pre class='raw'>{html.escape(path.read_text(encoding='utf-8'))}</pre>"
    elif path.name == "SKILL.md":
        _, desc, md_body = _parse_skill(path)
        intro = f"<p class='skill-desc'>{html.escape(desc)}</p>" if desc else ""
        body = intro + _sanitize(md_render(md_body, extensions=MD_EXTENSIONS))
    else:
        body = _sanitize(md_render(path.read_text(encoding="utf-8"), extensions=MD_EXTENSIONS))
    return render_template(
        "page.html", sections=catalog(), section=section, item=item, body=body,
        active=(section_key, slug),
    )


@app.route("/api/catalog")
def api_catalog():
    return jsonify(catalog())


@app.route("/api/health")
def api_health():
    # CHG-001.1: counts derive from the same live catalog scan the UI serves.
    docs, skills = _counts(catalog())
    return jsonify({"status": "ok", "documents": docs, "skills": skills})


def _identity_from_request() -> dict:
    """#10 out-of-scope note (its own ticket body): real SSO/OIDC is not
    built here — this is the documented stub identity carries until it is.
    Presence of the header is "authenticated"; it never carries roles yet
    (v1 authz policy doesn't check any)."""
    actor = request.headers.get("X-Harness-Actor", "").strip()
    return {"authenticated": bool(actor), "roles": []}


def _build_manifest_or_404(version: str) -> dict:
    try:
        return doctrine.build_manifest(ROOT, version, catalog())
    except KeyError:
        abort(404, description=f"unknown doctrine version: {version}")
    except doctrine.ManifestBuildError:
        # G5 finding: HARNESS_ROOT with no `.git` (or no `git` binary) must
        # fail closed cleanly, not crash with an unhandled 500 leaking a
        # subprocess traceback into server logs on every request.
        abort(500, description="doctrine manifest could not be built")


@app.route("/api/doctrine/<version>/manifest")
def api_doctrine_manifest(version: str):
    manifest = _build_manifest_or_404(version)
    identity = _identity_from_request()
    # Filter, don't just gate on fetch — ADR-002's RBAC amendment: the
    # service controls what enters context, including what a listing reveals.
    visible = [f for f in manifest["files"] if doctrine.is_allowed(identity, f)]
    return jsonify({**manifest, "files": visible})


@app.route("/api/doctrine/<version>/file")
def api_doctrine_file(version: str):
    manifest = _build_manifest_or_404(version)
    rel_path = request.args.get("path", "")
    entry = next((f for f in manifest["files"] if f["path"] == rel_path), None)
    if entry is None:
        abort(404, description="path not in manifest")
    identity = _identity_from_request()
    if not doctrine.is_allowed(identity, entry):
        abort(403, description="not authorized")
    try:
        return jsonify(doctrine.read_file_verified(ROOT, manifest, rel_path))
    except doctrine.IntegrityError:
        abort(500, description="content integrity check failed")


if __name__ == "__main__":
    app.run(host=os.environ.get("HOST", "127.0.0.1"),
            port=int(os.environ.get("PORT", "5050")), debug=False)
