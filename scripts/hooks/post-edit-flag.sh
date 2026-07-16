#!/usr/bin/env bash
# post-edit-flag.sh — PostToolUse hook (Edit|Write|NotebookEdit).
# Records that code changed since the last green verify run, by appending the
# touched path to .claude/.needs-verify. scripts/verify.sh clears the flag on
# ALL GREEN; scripts/hooks/stop-verify-check.sh blocks turn-end while it exists.
# Documentation-only paths don't set the flag.
set -uo pipefail

INPUT="$(cat)"
if command -v jq >/dev/null 2>&1; then
  FP="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
else
  FP="$(printf '%s' "$INPUT" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null || echo "")"
fi
[[ -z "$FP" ]] && exit 0

case "$FP" in
  *.md|*.markdown|*.log|*.txt|*/docs/*|*/.claude/*|*.gitignore) exit 0 ;;
esac

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
mkdir -p "$ROOT/.claude"
echo "$(date -u +%FT%TZ) $FP" >> "$ROOT/.claude/.needs-verify"
exit 0
