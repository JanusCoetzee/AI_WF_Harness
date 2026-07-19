# Harness browser (#9, ADR-002): read-only doctrine viewer. Content is a
# read-only volume mount; the image carries only the app. Run:
#   docker run --rm --read-only -p 5050:5050 \
#     -v /path/to/harness/repo:/harness:ro -e HARNESS_ROOT=/harness harness-browser
FROM python:3.12-slim

WORKDIR /srv
COPY app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

RUN useradd --system --uid 10001 harness
USER harness

ENV HARNESS_ROOT=/harness PORT=5050
EXPOSE 5050

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5050/api/health', timeout=2).status == 200 else 1)"

# --worker-tmp-dir /dev/shm keeps gunicorn's heartbeat files off the root fs,
# so the container runs under docker --read-only (ADR-001/ADR-002 posture).
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT} --workers 2 --worker-tmp-dir /dev/shm app.server:app"]
