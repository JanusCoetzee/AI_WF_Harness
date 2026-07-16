#!/usr/bin/env bash
# bash-guard.sh — Claude Code PreToolUse hook for the Bash tool.
# Blocks destructive / gate-bypassing commands at the tool layer.
# Exit 2 = block (stderr shown to the model). Exit 0 = allow.
set -uo pipefail

INPUT="$(cat)"

# Extract .tool_input.command (jq if available, python3 fallback)
if command -v jq >/dev/null 2>&1; then
  CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
else
  CMD="$(printf '%s' "$INPUT" | python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || echo "")"
fi
[[ -z "$CMD" ]] && exit 0

block() {
  echo "BLOCKED by harness bash-guard: $1" >&2
  echo "If genuinely needed, the human must run it themselves and log an override in docs/harness/DECISIONS.log." >&2
  exit 2
}

case "$CMD" in
  # History / branch destruction
  *"git push"*--force*|*"git push"*-f*)          block "force push (protected history)";;
  *"git reset --hard"*)                          block "git reset --hard (destroys work)";;
  *"git clean"*-*f*)                             block "git clean -f (deletes untracked files)";;
  *"git branch -D"*)                             block "force branch delete";;
  # Filesystem
  *"rm -rf /"*|*"rm -rf ~"*|*"rm -rf .."*)       block "recursive delete outside project scope";;
  # Pipe-to-shell
  *"curl "*"| sh"*|*"curl "*"| bash"*|*"wget "*"| sh"*|*"wget "*"| bash"*) block "pipe-to-shell";;
  # Infra / prod blast radius — humans trigger these (segregation of duties)
  *"terraform destroy"*)                         block "terraform destroy";;
  *"kubectl delete namespace"*)                  block "kubectl delete namespace";;
  *"DROP TABLE"*|*"drop table"*|*"DROP DATABASE"*|*"drop database"*) block "destructive SQL";;
  *"aws s3 rb"*|*"aws s3 rm"*--recursive*)       block "recursive S3 delete";;
esac

# Deploy/release triggers are human actions per OPERATING-MODEL.md
if [[ "$CMD" == *"git tag"* && "$CMD" == *prod* ]]; then
  block "production release tag (human-only action)"
fi

exit 0
