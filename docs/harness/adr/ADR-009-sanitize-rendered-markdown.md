# ADR-009 — Sanitize rendered markdown HTML before serving it (harness browser)

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-08-12 |
| Deciders | janus (Driver), on the AI pair's recommendation |
| REQs served | GH-14 |

## Context

`app/server.py`'s `page()` route renders every `.md` file the catalog scans
(docs, stages, gates, templates, skills) through `markdown()` and serves the
result with Jinja's `| safe` filter (`app/templates/page.html:10`) — required
because the output is real HTML (tables, code blocks), not because it's been
verified free of attacker-controlled markup. Python-Markdown passes raw
inline/block HTML in the source through unchanged by default, so any `.md`
file containing a `<script>` tag or event-handler attribute would execute in
the viewer's browser (GH-14). No doc in the repo exercises this today (RECON
grepped clean), but ADR-002/ADR-008 point this browser toward being a shared
service other BU instances pull content from — a wider, less-trusted set of
markdown authors over time. Fix now, while the blast radius is one file and
one route, not after the topology change lands.

## Options considered

### Option A — Sanitize rendered HTML with an allowlist (bleach)

- Sketch: after `md_render()`, pass the HTML through `bleach.clean()` with an
  allowlist matching exactly what `MD_EXTENSIONS` (`tables`, `fenced_code`,
  `sane_lists`) plus base markdown actually produce — headings, paragraphs,
  lists, tables, code/pre, blockquote, links (href only, no `javascript:`),
  emphasis — and strip everything else (scripts, iframes, event handlers,
  inline styles).
- Pros: keeps 100% of current legitimate rendering (RECON confirms the
  allowlist covers every construct in use); one well-maintained library
  (`bleach`, built on `html5lib`) rather than hand-rolled tag stripping;
  fails closed — anything not on the allowlist is dropped, not passed
  through.
- Cons: new dependency to track (pip-audit, version pin, license check); an
  allowlist can go stale if a future doc legitimately needs a tag not yet
  allowed (e.g. `<details>`) — visible as broken rendering, not a silent
  security gap, so an acceptable failure mode.
- Risks: none identified against current content (RECON: no doc uses raw
  HTML today).

### Option B — Disable raw HTML passthrough in python-markdown itself

- Sketch: python-markdown's `safe_mode` was removed upstream in 3.0; the
  documented replacement is an extension (e.g. a custom treeprocessor) that
  drops raw HTML nodes before rendering, no new dependency.
- Pros: no new dependency; fix stays inside the existing markdown pipeline.
- Cons: hand-rolled security-relevant code with no upstream maintenance,
  versus a library whose whole job is HTML sanitization; higher chance of a
  bypass (attribute-based XSS vectors, malformed-HTML parser differentials)
  that a purpose-built sanitizer already handles; the harness's own standards
  (CLAUDE.md §3) treat "roll your own" as the higher-risk path for exactly
  this class of boundary.
- Risks: silent bypass on an edge case (e.g. `<img onerror=...>` styled to
  look like a benign construct) is the failure mode that matters most here,
  and Option B is more exposed to it than a maintained allowlist sanitizer.

## Decision

Option A. `bleach` is a small, actively maintained, purpose-built dependency
for exactly this problem (allowlist HTML sanitization), and the harness's own
rule against inventing security-relevant logic when a vetted library exists
applies directly. Version pinned in `app/requirements.txt`; checked with
`pip-audit` before landing (clean at pin time, per CLAUDE.md §2 — never add a
dependency carrying a High/Critical vuln).

## Consequences

Easier: rendered output has a defined, enforced contract (the allowlist) —
"what markdown is allowed to do" is now a reviewable list instead of
"whatever python-markdown happens to emit." Harder: a legitimate future need
for a currently-disallowed tag shows up as stripped/broken rendering rather
than working silently — acceptable, since it's a visible failure caught by
the page rendering, not a covert one. Tripwire: if `bleach` stops being
maintained or a documented bypass lands, revisit — Option B (or a maintained
successor library) becomes the fallback.
