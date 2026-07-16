"""Harness Browser — serves the AI Workflow Harness (docs, stages, gates,
templates, skills, config) as a small web UI.

Run:  python3 app/server.py   →  http://localhost:5050
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from flask import Flask, abort, jsonify, render_template
from markdown import markdown as md_render

ROOT = Path(__file__).resolve().parent.parent
MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]

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

    cfg = ROOT / "harness.config.yaml"
    if cfg.exists():
        add("config", "Config", [{
            "slug": "harness-config",
            "title": "harness.config.yaml",
            "path": "harness.config.yaml",
            "desc": "Risk tiers, verify loop, fast-path policy, release policy",
        }])
    return sections


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
    doc_count = sum(len(s["items"]) for s in sections if s["key"] != "skills")
    return render_template(
        "index.html", sections=sections, skills=skills,
        greenfield=GREENFIELD, brownfield=BROWNFIELD,
        doc_count=doc_count, skill_count=len(skills),
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
        body = intro + md_render(md_body, extensions=MD_EXTENSIONS)
    else:
        body = md_render(path.read_text(encoding="utf-8"), extensions=MD_EXTENSIONS)
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
    sections = catalog()
    return jsonify({
        "status": "ok",
        "documents": sum(len(s["items"]) for s in sections if s["key"] != "skills"),
        "skills": sum(len(s["items"]) for s in sections if s["key"] == "skills"),
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
