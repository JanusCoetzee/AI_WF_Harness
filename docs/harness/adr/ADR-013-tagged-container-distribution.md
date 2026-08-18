# ADR-013 — Publish version-tagged, content-baked container images for exploring this harness's own doctrine; retro captures their metadata

| Field | Value |
| --- | --- |
| Status | Proposed |
| Date | 2026-08-19 |
| Deciders | janus (Driver) |
| REQs served | #8 (doctrine service distribution), #31 (container this builds on), the dev-team pilot's own feedback loop |

## Context

`#31` proved one image can serve both the browser and MCP endpoint, live,
under `--read-only`. Today's only distribution path is `git clone` +
`docker build` + `-v $(pwd):/harness:ro` — a dev builds the image
themselves and mounts *some* checkout into it. That checkout could be
this harness's own repo, or an adopting team's repo that vendored the
harness files in (`README.md`'s Quickstart) — the container itself
doesn't distinguish the two, it just serves whatever's mounted.

For the dev-team pilot specifically (README's "Try it: run the container
yourself," GH-31's follow-on), that flexibility is friction, not a
feature: the point is "explore *this* harness's doctrine and give
feedback," not "figure out which checkout to point it at." It also
foreshadows a real gap named in the AWS/ECS discussion (2026-08-18,
`DECISIONS.log`): ADR-002 already describes the target end state as
"this repo becomes a template repo with tagged releases... doctrine at
pinned versions (`harness-vX.Y` git tags)" — a `[content store]` box in
its system sketch that was never actually decided down to a mechanism.
Building the pilot's distribution and the eventual ECS deploy's content
sourcing on the *same* mechanism, instead of two divergent ones, is worth
deciding once rather than twice.

Separately, the Driver named a real gap in the pilot's feedback loop:
`pilot-feedback` issues (README, 2026-08-18) have no way to say *which*
code produced the experience being reported. With multiple tagged
versions potentially in the wild, retro (`stages/08-operate-learn.md`,
fortnightly) needs to correlate feedback to a version before triaging it
— the same "confirm the claim still holds" discipline ADR-006's drift
sweep already applies to `RECON.md` claims, applied to container/skills
versions instead.

## Options considered

### Option A — Status quo: git clone + docker build + bind-mount, unchanged

- Sketch: no change. Every pilot participant clones the repo, builds the
  image locally, mounts their own checkout.
- Pros: zero new infrastructure (no registry, no publish workflow); one
  Dockerfile, one mechanism, already proven at `#31`'s G4-equivalent
  evidence.
- Cons: doesn't solve the actual friction (onboarding requires a full
  clone + build before anyone sees anything); doesn't give retro anything
  to correlate feedback against beyond "whatever commit they happened to
  have checked out," which nobody reliably records; doesn't move the AWS
  content-sourcing question forward at all.
- Risks: the pilot's own stated purpose — gathering real signal — degrades
  quietly if feedback can't be tied to a version; "which commit were you
  on" becomes an unanswerable follow-up question on most issues.

### Option B — Replace the mount model entirely: always bake content into a tagged image

- Sketch: `Dockerfile` always `COPY`s doctrine content at build time
  (whichever repo's content is being packaged); the bind-mount pattern is
  removed. One image per tagged doctrine version, published to a
  registry, pulled and run with no mount at all.
- Pros: simplest possible mental model — one image, one version, no mount
  path to get wrong; directly reusable as-is for the eventual ECS deploy
  (Option 1 from the 2026-08-18 AWS discussion).
- Cons: **breaks the adopting-team use case this repo already documents
  and supports** (`README.md`'s Quickstart: a team vendors the harness
  into their own repo and serves their own copy). Forcing every adopter
  to rebuild-and-republish an image to serve their own doctrine is a
  regression from "mount your checkout, done."
- Risks: silently narrows this repo's own stated audience (harness
  adopters generally) to solve a problem specific to one audience (this
  repo's own pilot).

### Option C — Both mechanisms, same `Dockerfile`, different build target: mount mode (unchanged, default) + baked/tagged mode (new, published for this repo's own reference doctrine)

- Sketch: `Dockerfile` gains a build `ARG` (e.g. `CONTENT_MODE=mount`
  default, `CONTENT_MODE=baked` for tagged builds) controlling whether
  content is `COPY`'d in at build time or left to the existing runtime
  mount — one Dockerfile, two build outputs, not two Dockerfiles to keep
  in sync. On every `v*` git tag push, CI builds the `baked` variant from
  *this repo's own* content at that tag, labels it (Contracts below),
  and publishes it to a registry (GHCR — no AWS account/ECR dependency
  presumed, works today, doesn't front-run the still-undecided ECS
  question). Adopting teams keep using mount mode exactly as documented
  today, unchanged.
- Pros: solves the pilot's actual friction (`docker pull && docker run`,
  no clone/build) without regressing the adopting-team path; the tagged
  image becomes a real, reusable artifact for the AWS "bake into image"
  option too, decided once; every tagged image is self-describing
  (Contracts below) so retro has something concrete to correlate
  feedback against.
- Cons: two build outputs from one `Dockerfile` is more moving parts than
  Option A; a new publish workflow + registry is new infrastructure with
  its own supply-chain surface (named in Threat-model delta below, not
  glossed over).
- Risks: `CONTENT_MODE` is a real branch in the build; if it drifts
  (baked mode silently diverging from mount mode's actual runtime
  behavior) that's a new class of bug neither mode has today. Mitigated
  by both modes sharing the same app code and entrypoint — only *how
  `/harness` gets populated* differs, not what serves it.

## Decision

**Option C.** It's the only option that gets the pilot what it actually
needs (pull, don't build) without breaking the adopting-team path this
repo already promises, and it answers the AWS content-sourcing question
(2026-08-18) with the same mechanism instead of a second, divergent one
decided later under deploy pressure.

**Registry: GHCR** (`ghcr.io/janusCoetzee/harness-doctrine`), not ECR —
this repo has no AWS account provisioned yet and shouldn't presume one to
publish a pilot image; if/when real ECS deploy happens, GHCR → ECR
mirroring or a registry change is a separate, later decision, not blocking
this one.

**Tag discipline (extends ADR-002's "no `latest`" invariant to images,
not just doctrine versions):** published images are tagged explicitly
(`v0.2.0`, matching this repo's existing git tag convention — confirmed
`v0.2.0` already exists) — **no `:latest` tag is ever published.** A
`docker pull` with no explicit tag must fail or resolve to nothing usable,
the same fail-closed-on-unpinned posture the doctrine API already holds
for HTTP/MCP.

## Contracts (defined before implementation, per this repo's own pattern)

**OCI labels, baked into every published (`baked`-mode) image at build
time — queryable via `docker inspect`, no need to even run the
container:**

| Label | Value | Source |
| --- | --- | --- |
| `org.opencontainers.image.version` | the git tag (e.g. `v0.2.0`) | CI, from the tag ref |
| `org.opencontainers.image.revision` | full git commit SHA | CI, from the tagged commit |
| `io.harness.doctrine_version` | e.g. `harness-v0.2` | `harness.config.yaml`'s `doctrine.version` at build time — the same string already used throughout the HTTP/MCP API, not a new naming scheme |
| `io.harness.skills` | comma-separated `name@version` list | `harness.config.yaml`'s `doctrine.skills[]` at build time |

**Runtime confirmation, not just static labels:** the already-shipped
`GET /api/doctrine/{version}/manifest` route returns `git_commit` and
`skills[]` live (confirmed working, `#31`'s live proof) — a *running*
container is self-describing with zero new app code. Labels cover the
pulled-but-not-yet-run case; the manifest route covers the running case.
Both must agree (a mismatch would itself be a retro-worthy finding).

## Retro captures this metadata (the Driver's explicit ask)

`templates/RETRO.md` gains a new section, same shape as the existing
brownfield drift-sweep table:

```
## Pilot container/skills metadata sweep

For each `pilot-feedback` issue opened since the last retro: which image
tag and skills[] composition produced it, and is that still the current
published tag?

| Issue # | Image tag | git_commit (short) | skills[] versions | Still current tag? | Notes |
| --- | --- | --- | --- | --- | --- |
```

`.claude/skills/harness-retro/SKILL.md` gains a new numbered step (after
the existing brownfield drift sweep, same discipline applied to a new
axis): sweep every `pilot-feedback` issue opened since the last retro,
record its reported image tag/labels, and flag any that report against a
tag that's since been superseded — stale feedback gets triaged
differently from feedback against the current tag, the same way a stale
`RECON.md` claim is triaged differently from one that still holds.

`README.md`'s existing `pilot-feedback` ask gains one line: include the
output of `docker inspect --format='{{json .Config.Labels}}' <image>` (or
the `git_commit`/`skills[]` fields from `/api/health` if the container's
still running) in the issue.

## Threat-model delta (named up front, not deferred to whenever this is built)

A publish workflow + public-ish registry is a **new boundary**, not
covered by the existing `CI → ECR → ECS` row (that's a different
registry, different trust model). It's structurally the same shape
ADR-008 already modeled for the shared skill-artifact registry (`Shared
registry → BU build pipeline` row, `THREAT-MODEL.md`) — same mitigations
apply: only CI (via its OIDC role, no long-lived keys, matching the
existing `CI → ECR → ECS` pattern) can publish a tag; published tags are
immutable; content is still sha256-manifest-verified at serve time
regardless of which mode produced the image, so a tampered *image* still
can't serve tampered *content* without the existing fail-closed integrity
check catching it. **Not yet in `THREAT-MODEL.md`'s boundary table** —
adding that row is this ADR's own follow-on work at build time, not
optional.

## Escalation triggers — answer honestly (this ADR exists because one tripped)

| Trigger | Yes/No |
| --- | --- |
| New external interface, data flow, or LLM touchpoint? | **Yes — a new registry/publish path.** This is why this is an ADR and not a `CHANGE.md` fast-path item |
| Decision that deviates from the existing pattern? | Yes — new build-time branch (`CONTENT_MODE`), new CI job, new registry. Named and designed here, not discovered mid-build |
| Effort beyond ~3 days after recon? | Likely no for the packaging/labels/retro-template pieces; the CI publish workflow + registry setup is the real unknown, sized at build time |
| Tier raised during recon? | T2 stays T2 — content is unchanged (still Internal-max doctrine, no new data classification), the new surface is supply-chain, not data-sensitivity |

## Consequences

**Easier:** pilot onboarding drops to `docker pull && docker run`; retro
gets real, structured signal about which version produced which feedback
instead of guessing; the AWS content-sourcing question (2026-08-18) has a
decided, reusable answer instead of a second decision made later under
deploy pressure.

**Harder / new commitments:** a registry now exists and needs upkeep
(retention policy for old tags, access review); `CONTENT_MODE`'s two
build paths must be kept from silently diverging (mitigated by sharing
app code/entrypoint, not full isolation); `THREAT-MODEL.md` needs the new
boundary row before this ships, not after; the `pilot-feedback` issue
template/README instructions need the metadata-inclusion line added and
actually followed, which is a habit to establish, not just a doc change.

**Not decided here, deliberately:** whether/when to also publish to ECR
for a real ECS deploy — that's downstream of the still-open real-SSO/G7
decision, not this one.
