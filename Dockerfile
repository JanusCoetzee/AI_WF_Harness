# Harness doctrine service (#9 browser + #11 MCP, ADR-002; containerized
# together per GH-31). Content is a read-only volume mount; the image
# carries only the app. Run:
#   docker run --rm --read-only -p 5050:5050 -p 5051:5051 \
#     -v /path/to/harness/repo:/harness:ro -e HARNESS_ROOT=/harness harness-doctrine
FROM python:3.12-slim

# GH-31 finding: app/doctrine.py::_git_commit() shells out to `git
# rev-parse` for every manifest's provenance -- the base image never had
# `git`, so this was a latent defect in #10's already-shipped manifest
# route too, just never exercised through Docker (its own G4/G5 evidence
# was a bare local process, where dev-machine git was on PATH by
# coincidence). `.git` metadata itself comes from the mounted repo
# (read-only volume) -- only the binary needs to live in the image.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
COPY scripts/container-entrypoint.sh scripts/container-healthcheck.py scripts/
RUN chmod +x scripts/container-entrypoint.sh

RUN useradd --system --uid 10001 harness
USER harness

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
