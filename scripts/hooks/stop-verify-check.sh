#!/usr/bin/env bash
# stop-verify-check.sh — Stop hook: the turn does not end with unverified code.
# If .claude/.needs-verify exists (set by post-edit-flag.sh), block the stop and
# tell the model to either run scripts/verify.sh (clears the flag on ALL GREEN)
# or explicitly declare the work unverified via declare-unverified.sh.
# Warn-only when harness.config.yaml is still the unconfigured template.
# Exit 2 = block stop, exit 0 = allow.
set -uo pipefail

INPUT="$(cat)"
if command -v jq >/dev/null 2>&1; then
  ACTIVE="$(printf '%s' "$INPUT" | jq -r '.stop_hook_active // false')"
else
  ACTIVE="$(printf '%s' "$INPUT" | python3 -c 'import sys,json;print(str(json.load(sys.stdin).get("stop_hook_active",False)).lower())' 2>/dev/null || echo false)"
fi
# Loop safety: if a previous block already forced a continuation, let it end.
[[ "$ACTIVE" == "true" ]] && exit 0

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
FLAG="$ROOT/.claude/.needs-verify"
[[ ! -f "$FLAG" ]] && exit 0

# Unconfigured harness (fresh copy of the template): warn, don't block.
if grep -q 'name: CHANGE_ME' "$ROOT/harness.config.yaml" 2>/dev/null; then
  echo "harness: code changed without a verify run (warn-only until harness.config.yaml is configured)" >&2
  exit 0
fi

{
  echo "BLOCKED by harness stop-verify-check: code changed since the last green verify."
  echo "Do one of the following before ending the turn:"
  echo "  1. Run scripts/verify.sh  (clears this on ALL GREEN), or"
  echo "  2. Declare it: scripts/hooks/declare-unverified.sh '<reason>'  (logged, auditable)"
  echo "Changed since last verify:"
  sort -u "$FLAG" | tail -10
} >&2
exit 2
