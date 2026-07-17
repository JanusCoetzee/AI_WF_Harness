# RECON — GH-6

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Catalog builder | app/server.py:52 `catalog()` | sections built via `add()`; new section follows the existing pattern |
| YAML rendering path | app/server.py `page()` suffix check | already renders .yaml as raw — ground truths reuse it |
| Title extraction | app/server.py:21 `_title_of` | reads first `# ` line; works for YAML comment headers too |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| tests/test_characterization.py | pins /api/catalog section-key list | the pin moves DELIBERATELY in this change's diff (GH-6.3) |
| humans in a browser | sidebar/library render new section automatically | template iteration is data-driven |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| Section order ends with "config" | pinned test | kept — evals inserted before config |
| Item dict shape {slug,title,path,desc} | pinned test | unchanged; new items conform |

## Test coverage reality

- Existing: 16 tests incl. catalog shape pin.
- Added: tests/test_evals_browsable.py (GH-6.1/.2), written red first (3 failed
  pre-implementation), green post. Section pin moved with an in-diff comment.

## Surprises / archaeology

None — single-file change in a well-pinned app.

## Go / No-go

- [x] Blast radius confirmed; [x] characterization pins honored (one moved, visibly)
- **Recommendation:** go
