# RECON — #32 (publish version-tagged, content-baked images to GHCR)

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Current single-stage `Dockerfile` | `Dockerfile` | Always mount-mode; `#31` added the two-process entrypoint/healthcheck but content is always a runtime volume |
| `.dockerignore` | `.dockerignore` | Blanket-excludes `docs`, `evals`, `gates`, `stages`, `templates`, `.claude`, `.git` — fine when content is always mounted, **directly conflicts with baked mode's need to `COPY` that same content in** |
| What `catalog()` actually scans | `app/server.py:89-110` | `docs/*.md`, `stages/*.md`, `gates/*.md`, `templates/*.md`, `.claude/skills/*/SKILL.md` — this is the exact set baked mode must include, nothing more |
| `_git_commit()` | `app/doctrine.py` (per `#31`'s own finding) | shells out to `git rev-parse` against `HARNESS_ROOT` — baked mode needs a real `.git/` present under `/harness`, not just files |
| Existing tag convention | `git tag -l` → `v0.2.0` | Confirmed, reused as-is — no new tagging scheme invented |
| Repo visibility | `gh repo view --json visibility` → `PUBLIC` | GHCR publish from a public repo works with the workflow's own built-in `GITHUB_TOKEN` (`permissions: packages: write`) — **no new secret needs provisioning** |
| Existing carve-out precedent | `.dockerignore` (from `#31`) | `!scripts/container-entrypoint.sh` / `!scripts/container-healthcheck.py` already proves per-file negation under a broader exclusion works in this Docker/buildx version — same technique extends to directories |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| Local dev / adopting teams | `docker build .` with no args — must stay byte-identical (AC #2) | `README.md`'s existing Quickstart/pilot instructions |
| `.github/workflows/verify.yml` | doesn't touch Docker at all today (`grep -rn docker .github/` — no hits before this ticket) | grep |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| `docker build -t x .` with no `--build-arg` produces mount-mode | `Dockerfile` today (only mode that exists) | Must stay true — `CONTENT_MODE` defaults to `mount`, unnamed builds are unaffected |
| `.dockerignore` strips `docs/`/`gates/`/`stages/`/`templates/`/`.claude/`/`.git` from every build's context | current file | **Changing, deliberately, named below** — negating these for baked mode's `COPY` to see them also means mount-mode's build *context upload* gets marginally larger (more bytes sent to the daemon), even though mount-mode's *resulting image* is unaffected (its stage never `COPY`s the newly-unignored paths). This is a real, disclosed cost — not a behavior regression under AC #2's own definition (served behavior, not build performance), but named here so it isn't discovered as a surprise later |

## A real design fork found during recon, resolved here — named, not silently picked

Two ways to get baked-mode content past `.dockerignore`'s exclusions were tested live:

1. **`docker buildx build --build-context content=<other-path>`** — a named
   build context bypasses the *default* context's `.dockerignore`
   **only when it points at a directory that doesn't itself have a
   `.dockerignore`.** Tested live: pointing the named context at a
   *different* directory worked; pointing it at the **same** directory as
   the Dockerfile (this repo's actual shape — content and `Dockerfile`
   live in the same tree) did **not** — the same `.dockerignore` still
   applied. This would require CI to check out the repo twice into
   different paths just to route around it — real, avoidable complexity.
2. **Negate the specific paths in `.dockerignore` itself** (the same
   technique `#31` already used and proved for the two container
   scripts), applied to `docs`, `evals`, `gates`, `stages`, `templates`,
   `.claude/skills`, `.git`. Simpler, no extra checkout, no named-context
   plumbing — the cost is the marginally larger context upload named
   above, accepted as reasonable for this repo's size.

**Chosen: option 2.** Verified empirically (not assumed) that Docker's
negation matching works for nested subpaths under an excluded parent —
confirmed with a throwaway test build before touching the real
`.dockerignore`.

## Test coverage reality

No existing test drives Docker builds (consistent with `#9`'s/`#31`'s own
precedent — bash/Docker, outside `pytest`'s scope). This ticket adds no
new `pytest` coverage; its evidence is two live, reproduced
`docker build` runs (mount and baked) plus a real tag-triggered GHCR
publish, same rigor `#31` was held to.

## Go / No-go

- [x] Blast radius confirmed: `Dockerfile`, `.dockerignore`, one new
  GitHub Actions job, `THREAT-MODEL.md` — no application code
- [x] Mount-mode's own build path re-verified unaffected after the
  `.dockerignore` negation (live diff of resulting image layers, not
  assumed)
- [x] No consumer contract broken — mount-mode default preserved exactly
- **Recommendation:** go
