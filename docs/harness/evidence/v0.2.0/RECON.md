# RECON — CHG-001

Understanding before changing. Every claim about existing behavior cites `file:line`
or a test — no claims from memory.

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Existing API route to extend alongside | app/server.py:150-152 (`/api/catalog`) | returns `jsonify(catalog())` |
| Catalog builder (source of counts) | app/server.py:52-90 (`catalog()`) | rescans repo per request; sections incl. `skills` |
| Home route to surface counts | app/server.py:121-129 (`index()`) | already extracts `skills` list for cards |
| Hero template block to extend | app/templates/index.html:3-7 (`.hero`) | one line added under the tagline |
| Server bind | app/server.py:156 | 127.0.0.1:5050, debug off — no reload; restart IS the deploy |

## Consumers found

| Consumer | How it depends on touched behavior | Found via |
| --- | --- | --- |
| Humans in a browser | render of `/` hero | only UI surface |
| None programmatic | `grep -r "api/catalog"` finds only README/base.html links; no scripts call it | grep + driver confirmation |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence (file:line / test) | Safe to change? |
| --- | --- | --- |
| `/api/catalog` section order overview→config | tests/test_characterization.py::test_catalog_sections_and_shape | not touched; pinned |
| Item dict shape exactly {slug,title,path,desc} | same test | not touched; pinned |
| Unknown API paths return 404 | tests/test_characterization.py::test_unknown_paths_404 | `/api/health` 404 is pinned and will change DELIBERATELY (CHG-001.1) — the change commit must update that assertion visibly |

## Test coverage reality

- Existing tests covering the touched path: **none existed** — the app shipped with
  route-level curl smoke checks only (a drill finding for the retro).
- **Characterization tests added:** tests/test_characterization.py (6 tests, green
  against unchanged code — run recorded below).
- Behaviors deliberately left unpinned: exact HTML styling; markdown renderer output
  details (third-party).

## Surprises / archaeology

| Finding | Action (retro-ADR-### / accepted as-is) |
| --- | --- |
| App had no test harness at all; verify `test` step was empty | Fixed as part of this change: pytest wired into verify — flagged for retro |

## Revised blast radius & tier

Unchanged from CHANGE.md. Effort: hours. Tier stays T2. No escalation triggers
tripped after recon.

## Go / No-go

- [x] Blast radius confirmed, no "unknown" rows above
- [x] Characterization tests green against unchanged code (6 passed, 0.71s)
- [x] Escalation triggers re-checked after what recon revealed
- **Recommendation:** go — single-route addition with pinned surroundings
