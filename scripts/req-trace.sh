#!/usr/bin/env bash
# req-trace.sh — full REQ-###/CHG-### traceability table (ADR-005), replacing
# the manual "pick 3 REQs" spot-check at G5 with a scripted full trace.
# Collects every REQ-###/CHG-###.n from PRD.md and changes/*/CHANGE.md, then
# greps for each across ADRs, PLAN.md, tests/, and git log — one row per ID.
# An ID with no hit in any category is a broken trace and fails the check.
# Usage: scripts/req-trace.sh [--md]   (--md writes docs/harness/evidence/req-trace-<ts>.md)
set -uo pipefail

H="${HARNESS_DIR:-docs/harness}"
IDS=()

collect_ids() {
  local f="$1"
  [[ -f "$f" ]] || return 0
  # Same ticket-key shape scripts/hooks/commit-guard.sh already accepts
  # (REQ-###, CHG-###, and any short-prefix key like GH-17.1, FIN-4821),
  # plus the optional .n acceptance-criteria suffix commit-guard.sh doesn't need.
  grep -oE '[A-Z][A-Z0-9]{1,9}-[0-9]+(\.[0-9]+)?' "$f"
}

while IFS= read -r id; do
  IDS+=("$id")
done < <(
  { collect_ids "$H/PRD.md"; for c in "$H"/changes/*/CHANGE.md; do collect_ids "$c"; done; } \
    | sort -u
)

if [[ ${#IDS[@]} -eq 0 ]]; then
  echo "req-trace: no REQ-###/CHG-### ids found in $H/PRD.md or $H/changes/*/CHANGE.md"
  exit 0
fi

hit() {
  local id="$1" path="$2"
  [[ -e "$path" ]] || return 1
  grep -rqE "$(printf '%s' "$id" | sed 's/\./\\./g')" "$path" 2>/dev/null
}

echo "| ID | ADR | PLAN | tests | commits |"
echo "| --- | --- | --- | --- | --- |"

FAILS=0
for id in "${IDS[@]}"; do
  a="✗"; p="✗"; t="✗"; c="✗"
  hit "$id" "$H/adr" && a="✓"
  hit "$id" "$H/PLAN.md" && p="✓"
  hit "$id" "tests" && t="✓"
  git log --oneline -F --grep="$id" >/dev/null 2>&1 && [[ -n "$(git log --oneline -F --grep="$id" 2>/dev/null)" ]] && c="✓"

  echo "| $id | $a | $p | $t | $c |"

  if [[ "$a$p$t$c" == "✗✗✗✗" ]]; then
    FAILS=$((FAILS+1))
  fi
done

echo
if [[ $FAILS -gt 0 ]]; then
  echo "req-trace: ✗ $FAILS id(s) with zero hits across ADR/PLAN/tests/commits" >&2
else
  echo "req-trace: ✓ every id traces to at least one artifact"
fi

if [[ "${1:-}" == "--md" ]]; then
  mkdir -p "$H/evidence"
  OUT="$H/evidence/req-trace-$(date +%Y%m%d-%H%M%S).md"
  "$0" > "$OUT" 2>/dev/null || true
  echo "written: $OUT"
fi

exit $((FAILS > 0 ? 1 : 0))
