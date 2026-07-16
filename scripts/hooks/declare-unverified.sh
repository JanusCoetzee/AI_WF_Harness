#!/usr/bin/env bash
# declare-unverified.sh — the auditable escape hatch for stop-verify-check.
# Clears the needs-verify flag by *recording* that work is unverified, never by
# pretending it was verified. Appends to DECISIONS.log (or .claude/UNVERIFIED.log
# if the harness artifacts dir doesn't exist yet).
# Usage: scripts/hooks/declare-unverified.sh "<reason>"
set -euo pipefail

REASON="${1:?usage: declare-unverified.sh \"<reason>\"}"
ROOT="${CLAUDE_PROJECT_DIR:-$(pwd)}"
FLAG="$ROOT/.claude/.needs-verify"

FILES="none recorded"
[[ -f "$FLAG" ]] && FILES="$(sort -u "$FLAG" | awk '{print $2}' | tr '\n' ' ')"

TARGET="$ROOT/docs/harness/DECISIONS.log"
[[ -d "$ROOT/docs/harness" ]] || TARGET="$ROOT/.claude/UNVERIFIED.log"
mkdir -p "$(dirname "$TARGET")"

echo "$(date -u +%F) | UNVERIFIED | $(whoami) | $REASON | files: $FILES" >> "$TARGET"
rm -f "$FLAG"
echo "declared UNVERIFIED in $TARGET — remember to reflect this in STATE.md; G4 cannot pass while it stands."
