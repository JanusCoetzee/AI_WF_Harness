# RECON — GH-14

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Markdown render | app/server.py `page()` — `md_render(path.read_text(...), extensions=MD_EXTENSIONS)` (~line 183) | `MD_EXTENSIONS = ["tables", "fenced_code", "sane_lists"]` (server.py:25); python-markdown passes raw inline/block HTML through unchanged by default |
| Skill body render | app/server.py `page()` — SKILL.md branch (~line 179-181) | same `md_render` call, plus an `intro` built with `html.escape(desc)` — the frontmatter `desc` is already escaped, only the body is not |
| Unsafe sink | app/templates/page.html:10 | `{{ body | safe }}` — Jinja autoescaping is disabled for this one variable, everything upstream must already be safe HTML |
| Raw-YAML path (contrast) | app/server.py `page()`, `.yaml`/`.yml` branch (~line 176-177) | already uses `html.escape()` — this branch is NOT affected, only the two markdown branches are |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| `/s/<section>/<slug>` route | renders `body` for every doc/stage/gate/template/skill page | only call site of `page.html` |
| tests/test_characterization.py::test_document_page_renders_markdown | pins `<table>` present in output | grep of tests |
| tests/test_characterization.py::test_skill_page_shows_description | pins `skill-desc` class present | grep of tests |
| tests/test_evals_browsable.py::test_eval_pages_render | pins 200 status for eval pages incl. raw YAML | grep of tests |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| `<table>`, `<code>`, `<pre>`, `<h1-6>`, `<a href>`, `<blockquote>`, `<ul>/<ol>/<li>`, `<strong>/<em>` render as real markup (from `tables`/`fenced_code`/`sane_lists` + base markdown) | every doc page in the repo uses these; pinned by test_document_page_renders_markdown | keep — allowlist must include exactly this set |
| Raw HTML embedded directly in a `.md` source file renders as live markup | default python-markdown behavior, not exercised by any current repo doc (grepped — no `.md` file under docs/stages/gates/templates/.claude/skills contains raw HTML tags today) | **not** safe — this is the defect; no current doc relies on it |
| SKILL.md `desc` (frontmatter) already escaped via `html.escape` | app/server.py `page()` SKILL.md branch | unchanged by this fix |

## Test coverage reality

- 21 existing tests pass; none currently probes for HTML injection (no red test pins the vulnerable behavior — the defect was unexercised, not merely unguarded).
- Added (this change): a scratch markdown fixture rendered through `page()` asserting a `<script>`-bearing source produces no executable `<script>` tag in the response, run red-first against the pre-fix code, green after.

## Surprises / archaeology

No repo doc currently contains raw HTML — the vulnerable path is latent, not exercised by any existing content. Confirmed via `grep -rlE '<(script|iframe|on[a-z]+=)' docs/ stages/ gates/ templates/ .claude/skills/` → no hits. This means the fix carries no risk of breaking an existing doc's rendering (nothing today depends on raw-HTML passthrough).

## Go / No-go

- [x] Blast radius confirmed (single render path, two call sites, no doc depends on raw HTML today)
- [x] Characterization test added pre-fix, pins the gap before closing it
- **Recommendation:** go
