# Harness doctrine service (#9 browser + #11 MCP, ADR-002; containerized
# together per GH-31). Two content modes (GH-32/ADR-013), one Dockerfile:
#
#   mount (default, unchanged since #31) -- content is a read-only volume
#   mount, the image carries only the app:
#     docker build -t harness-doctrine .
#     docker run --rm --read-only -p 5050:5050 -p 5051:5051 \
#       -v /path/to/repo:/harness:ro -e HARNESS_ROOT=/harness harness-doctrine
#
#   baked (GH-32) -- this repo's own doctrine content is copied in at
#   build time; published, version-tagged images (GHCR) run with no
#   mount at all:
#     docker build --build-arg CONTENT_MODE=baked -t harness-doctrine:baked .
#     docker run --rm --read-only -p 5050:5050 -p 5051:5051 harness-doctrine:baked
ARG CONTENT_MODE=mount

FROM python:3.12-slim AS base

# GH-31 finding: app/doctrine.py::_git_commit() shells out to `git
# rev-parse` for every manifest's provenance -- the base image never had
# `git`. In mount mode `.git` comes from the mounted repo; in baked mode
# (below) `.git` is copied in too, so this binary is needed either way.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY scripts/container-entrypoint.sh scripts/container-healthcheck.py scripts/
RUN chmod +x scripts/container-entrypoint.sh

RUN useradd --system --uid 10001 harness

# GH-32 finding: app/doctrine.py::_git_commit() (via `git rev-parse`)
# fails with "detected dubious ownership" when /harness is owned by a
# different uid than the process running git -- true for baked mode's
# root-owned COPY'd content read by the non-root `harness` user, and a
# latent risk for mount mode too (it happened not to trip under Docker
# Desktop's bind-mount ownership reporting, which isn't a guarantee on
# every host/filesystem). `--system` scope (not `--global`, which needs a
# writable HOME the `--system`-flagged harness user doesn't have) fixes
# both modes at once, applies regardless of which user runs git.
RUN git config --system --add safe.directory /harness

# --- mount mode: unchanged, no content copied, runtime volume required ---
FROM base AS mount

# --- baked mode (GH-32): this repo's own doctrine content copied in at
# build time. .dockerignore negates exactly these paths for this reason
# (docs/harness/changes/GH-32/RECON.md's "design fork" section) -- named
# build-context tricks don't work here since the content lives in the
# same tree as this Dockerfile, so the same .dockerignore applies to
# them too; the negation is the simpler, verified-working fix. Mount
# mode's stage above never COPYs these paths, so its image is byte-
# identical to before this ticket (GH-32.2) even though the *build
# context upload* is marginally larger for every build now. ---
FROM base AS baked
COPY harness.config.yaml /harness/harness.config.yaml
COPY docs/ /harness/docs/
COPY evals/ /harness/evals/
COPY gates/ /harness/gates/
COPY stages/ /harness/stages/
COPY templates/ /harness/templates/
COPY .claude/skills/ /harness/.claude/skills/
COPY .git/ /harness/.git/

# --- final: whichever mode CONTENT_MODE selected ---
FROM ${CONTENT_MODE} AS final
WORKDIR /srv
USER harness

# OCI labels (ADR-013 Contracts): queryable via `docker inspect` with no
# container run needed. Only meaningful for baked/published images -- CI
# passes real values on publish; unset for local/mount builds (harmless).
ARG IMAGE_VERSION=""
ARG IMAGE_REVISION=""
ARG DOCTRINE_VERSION=""
ARG SKILLS_LABEL=""
LABEL org.opencontainers.image.version="${IMAGE_VERSION}" \
      org.opencontainers.image.revision="${IMAGE_REVISION}" \
      io.harness.doctrine_version="${DOCTRINE_VERSION}" \
      io.harness.skills="${SKILLS_LABEL}"

ENV HARNESS_ROOT=/harness PORT=5050 MCP_HOST=0.0.0.0 MCP_PORT=5051
EXPOSE 5050 5051

# scripts/container-healthcheck.py checks both processes and prints which
# one failed (GH-31) -- Docker itself only surfaces a single pass/fail bit
# per container; see RECON.md at docs/harness/changes/GH-31/.
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD python scripts/container-healthcheck.py

# scripts/container-entrypoint.sh runs both processes as independent
# foreground children (gunicorn is WSGI, mcp.run() is its own blocking
# event loop -- they can't share one process model) and deliberately does
# not kill one when the other dies (GH-31.6) -- gunicorn's own
# --worker-tmp-dir /dev/shm keeps it off the root fs so both processes run
# fully under docker --read-only (ADR-001/ADR-002 posture).
CMD ["scripts/container-entrypoint.sh"]
