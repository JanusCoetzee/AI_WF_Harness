#!/usr/bin/env bash
# session-start.sh — SessionStart hook: the session-start protocol as structure,
# not memory. Injects harness state into context automatically (stdout of a
# SessionStart hook is added to the model's context).
set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
STATE="$ROOT/docs/harness/STATE.md"

echo "=== AI Workflow Harness — state auto-loaded by SessionStart hook ==="
if [[ -f "$STATE" ]]; then
  cat "$STATE"
  DLOG="$ROOT/docs/harness/DECISIONS.log"
  if [[ -f "$DLOG" ]]; then
    echo
    echo "--- last decisions ---"
    tail -5 "$DLOG"
  fi
  if [[ -f "$ROOT/.claude/.needs-verify" ]]; then
    echo
    echo "!! OUTSTANDING: code changed without a green verify run (.claude/.needs-verify)"
  fi
else
  echo "No active work item (docs/harness/STATE.md not found)."
  echo "Run /harness-status to initialize, /harness-ideate for new work,"
  echo "or /harness-change for a change to existing code."
fi
exit 0
