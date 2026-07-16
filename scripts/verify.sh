#!/usr/bin/env bash
# verify.sh — the verify loop: typecheck → lint → test → eval → build.
# Reads commands from harness.config.yaml `verify:` block. Fails fast.
# Usage: scripts/verify.sh [--log]   (--log tees output into docs/harness/evidence/)
set -uo pipefail

CONFIG="${HARNESS_CONFIG:-harness.config.yaml}"
LOG=""
[[ "${1:-}" == "--log" ]] && LOG="docs/harness/evidence/verify-$(date +%Y%m%d-%H%M%S).log"

if [[ ! -f "$CONFIG" ]]; then
  echo "verify: $CONFIG not found (set HARNESS_CONFIG or run from repo root)" >&2
  exit 1
fi

# Extract a command from the verify: block (naive YAML read — one level, quoted values).
get_cmd() {
  awk -v key="$2" '
    /^verify:/ { in_block=1; next }
    in_block && /^[^[:space:]]/ { in_block=0 }
    in_block {
      line=$0
      sub(/#.*$/, "", line)                       # strip comments
      if (line ~ "^[[:space:]]+" key ":") {
        sub("^[[:space:]]+" key ":[[:space:]]*", "", line)
        gsub(/^"|"[[:space:]]*$/, "", line)
        print line
      }
    }' "$1"
}

run_step() {
  local name="$1" cmd="$2"
  if [[ -z "$cmd" ]]; then
    printf '  ~ %-10s skipped (not configured)\n' "$name"
    return 0
  fi
  printf '  > %-10s %s\n' "$name" "$cmd"
  local start=$SECONDS
  if bash -c "$cmd"; then
    printf '  ✓ %-10s ok (%ss)\n' "$name" "$((SECONDS - start))"
  else
    local rc=$?
    printf '  ✗ %-10s FAILED (exit %s) — stopping. Fix before proceeding.\n' "$name" "$rc" >&2
    exit "$rc"
  fi
}

main() {
  echo "verify loop @ $(git rev-parse --short HEAD 2>/dev/null || echo 'no-git') — $(date -u +%FT%TZ)"
  for step in typecheck lint test eval build; do
    run_step "$step" "$(get_cmd "$CONFIG" "$step")"
  done
  echo "verify: ALL GREEN"
}

if [[ -n "$LOG" ]]; then
  mkdir -p "$(dirname "$LOG")"
  main 2>&1 | tee "$LOG"
  exit "${PIPESTATUS[0]}"
else
  main
fi
