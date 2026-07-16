#!/usr/bin/env bash
# commit-guard.sh — PreToolUse hook (Bash): traceability is not optional.
# Blocks `git commit` unless the message references a work item:
#   REQ-### / CHG-### / Jira-style key (ABC-123) / GitHub issue (#123)
# Deliberate escape hatch (auditable, greppable): a `NO-TICKET: <reason>` line.
# Exit 2 = block, exit 0 = allow.
set -uo pipefail

INPUT="$(cat)"
if command -v jq >/dev/null 2>&1; then
  CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
else
  CMD="$(printf '%s' "$INPUT" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")"
fi
[[ -z "$CMD" ]] && exit 0
[[ "$CMD" != *"git commit"* ]] && exit 0

# Amend without a new message keeps the (already-guarded) original message.
if [[ "$CMD" == *"--amend"* && "$CMD" != *" -m"* && "$CMD" != *"--message"* ]]; then
  exit 0
fi

# The commit message is embedded in the command string; check it for an ID.
if printf '%s' "$CMD" | grep -qE 'REQ-[0-9]+|CHG-[0-9]+|[A-Z][A-Z0-9]{1,9}-[0-9]+|#[0-9]+|NO-TICKET:'; then
  exit 0
fi

{
  echo "BLOCKED by harness commit-guard: commit message has no work-item reference."
  echo "Every commit references what it serves: a ticket key (FIN-4821, #123),"
  echo "REQ-### or CHG-###. If this work genuinely has no ticket, include a line:"
  echo "  NO-TICKET: <reason>"
  echo "which is deliberate, greppable, and shows up in audit."
} >&2
exit 2
