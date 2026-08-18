# CHANGE — #32 Publish version-tagged, content-baked harness-doctrine images to GHCR

| Field | Value |
| --- | --- |
| Status | Drafted — awaiting Driver GC approval (CLAUDE.md §7: gate passage is human-only) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #32 — ADR-013's implementation, split from #33 |
| Date | 2026-08-19 |
| Risk tier | T2 — internal deploy tooling; content is unchanged Internal-max doctrine, new surface is supply-chain (registry), not data-sensitivity |
| Recon | required — see `RECON.md` |
| Linked records | `ADR-013` (accepted 2026-08-19, this ticket's design authority), `#31` (the container this builds on), `ADR-002`'s "no latest" invariant, `ADR-008`'s already-modeled shared-registry mitigations (reused, not reinvented) |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop — this ticket's proof is live builds/publishes, not assertions), §3 (schema/contract: OCI labels defined before implementation, mirroring ADR-002's own "Contracts" pattern), §8 (brownfield — cite file:line, RECON's design-fork section) |

## Intent

Publishing to GHCR is genuinely new external surface — `ADR-013` already
named this as its own escalation trigger and was written and accepted
*before* this build, satisfying the trigger's intent (same pattern
GH-14/ADR-009 established: escalation tripped, ADR written pre-build,
still fast-path afterward — see Escalation triggers below). Done means: a
`docker build --build-arg CONTENT_MODE=baked` run serves this repo's own
doctrine with **no volume mount at all**; mount-mode is byte-identical to
today; every published image carries the four OCI labels ADR-013's
Contracts section specifies; a real `v*` tag push publishes exactly that
tag to GHCR, never `:latest`; and `THREAT-MODEL.md` has its new registry
boundary row before this ships.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-32.1 | Given `docker build --build-arg CONTENT_MODE=baked -t harness-doctrine:test .`, when run with **no `-v` mount**, then it serves this repo's own doctrine correctly (browser `200`, MCP `initialize`→`tools/list`→`tools/call`, fail-closed `401` — same live checks `#31` proved) |
| GH-32.2 | Given the same build with `CONTENT_MODE=mount` (or omitted — the default), when run exactly as `#31`'s README instructions describe, then behavior is byte-identical to today |
| GH-32.3 | Given a built `baked`-mode image, when inspected (`docker inspect --format='{{json .Config.Labels}}'`), then all four labels (`image.version`, `image.revision`, `io.harness.doctrine_version`, `io.harness.skills`) are present and correct with no container run required |
| GH-32.4 | Given a `v*` git tag pushed to `main`, when CI runs, then a `baked`-mode image tagged with that exact version is published to GHCR, and **no `:latest` tag is ever published** — verified by checking the registry's actual tag list |
| GH-32.5 | Given `THREAT-MODEL.md`, when this ships, then it has a new boundary row for `registry → dev pull`, not left for later |

## Real findings from live testing (not asserted — reproduced, then fixed)

Two things `#31`'s testing never exercised, because baked mode is new:

1. **`build_manifest()` also reads `harness.config.yaml`** (the ADR-008
   composition pin) from `HARNESS_ROOT`, not just the `docs/`/`gates/`/etc.
   content — missed on the first baked-mode attempt (500,
   `FileNotFoundError`), reproduced live, fixed by adding it to the
   `baked` stage's `COPY` list.
2. **Git's "dubious ownership" check** rejects `git rev-parse` when
   `/harness` is owned by a different uid than the process running it —
   true for baked mode's root-owned `COPY`'d content read by the
   non-root `harness` user. Reproduced live (`fatal: detected dubious
   ownership in repository`), fixed with `git config --system --add
   safe.directory /harness` in the image. **This is a latent risk for
   mount mode too** — it happened not to trip under Docker Desktop's
   bind-mount ownership reporting during testing, which isn't a portable
   guarantee across hosts/filesystems — so the fix applies to both modes,
   not just baked.

## Live proof (2026-08-19)

```
$ docker build -t harness-doctrine:mount-test .                       # unchanged path, byte-identical (GH-32.2)
$ docker run --rm harness-doctrine:mount-test sh -c "ls /harness"
    -> No such file or directory (correctly: no content baked, mount still required)

$ docker build --build-arg CONTENT_MODE=baked \
    --build-arg IMAGE_VERSION=v0.2.0-test --build-arg IMAGE_REVISION=$(git rev-parse HEAD) \
    --build-arg DOCTRINE_VERSION=harness-v0.2 --build-arg SKILLS_LABEL="..." \
    -t harness-doctrine:baked-test .
$ docker inspect --format='{{json .Config.Labels}}' harness-doctrine:baked-test
    -> all four labels present and correct, zero container run needed    (GH-32.3)
$ docker run --rm --read-only -p 5050:5050 -p 5051:5051 harness-doctrine:baked-test   # NO -v mount
$ curl localhost:5050/api/doctrine/harness-v0.2/manifest
    -> real manifest, git_commit correct, skills[] correct (3 entries)   (GH-32.1)
$ curl (no auth) .../mcp -> 401                                          (fail-closed, unchanged)
$ curl (Bearer token) initialize -> tools/call harness_search_doctrine
    -> real content, no mount involved at all                            (GH-32.1)
$ docker exec ... id -> uid=10001(harness)                               (non-root, unchanged)
$ docker logs ... | grep -i "read-only|permission denied" -> clean       (GH-32.1, --read-only holds)
```

All local build-mode acceptance criteria (GH-32.1–3) verified live, not
asserted. `.github/workflows/publish-image.yml` (GH-32.4) is written and
YAML-validated (`python3 -c "import yaml; yaml.safe_load(...)"`) but
**deliberately not exercised with a real tag push in this session** — a
real `v*` tag publishes a real, public GHCR package under the Driver's
own GitHub account, which is an outward-facing action worth explicit
confirmation first, not something to do unasked mid-build. `THREAT-MODEL.md`'s
new registry boundary row (GH-32.5) is written.

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `Dockerfile` (multi-stage, `CONTENT_MODE` arg), `.dockerignore` (negated paths, named in RECON), new `.github/workflows/publish-image.yml`, `docs/harness/changes/GH-8/THREAT-MODEL.md` |
| Known consumers | none yet publicly (this is additive — no existing consumer pulls a tagged image today); local mount-mode users (README's documented flow) — explicitly preserved unchanged |
| Data elements | none new — same Internal-max doctrine content `#9`/`#10`/`#11` already serve and G6-cleared |
| Deploy surface | new: GHCR as a registry target, one new CI job triggered on `v*` tags. No AWS/ECR dependency — deliberately deferred (ADR-013's own "Not decided here" note) |

## Rollback note

Revert the commit. `Dockerfile`'s default (`CONTENT_MODE=mount`, unnamed
builds) is unaffected either way. A bad published tag can be deleted from
GHCR directly (registry operation, not a code rollback) — tags are
immutable once published (GH-32.4), so "fix and republish under the same
tag" is never the remediation; a new tag is.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | **Yes — new registry/publish path.** Satisfied: `ADR-013` written and accepted *before* this build (2026-08-19), exactly the trigger's own remedy | G2 — satisfied by the existing ADR, not re-run |
| Decision that deviates from the existing pattern? | No beyond what `ADR-013` already decided and ratified — this ticket implements that decision, doesn't make a new one | ADR |
| Effort beyond ~3 days after recon? | No — Dockerfile/labels/`.dockerignore` work is hours; the publish workflow is the real unknown but bounded (public repo, no new secrets needed per RECON) | G1 |
| Tier raised during recon? | No — stays T2 | re-approve |

## GC sign-off

T2: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-19 | GC passed | janus | GH-32`
