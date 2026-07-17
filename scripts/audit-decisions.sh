#!/usr/bin/env bash
# audit-decisions.sh — mechanical cross-check: every audit CLAIM in harness
# artifacts has its matching DECISIONS.log line. A gate passage that isn't
# logged didn't happen; this script makes the inverse true too — an unlogged
# claim fails verify (and therefore the stop hook and CI).
# Scans docs/harness only; evals/ runs are simulated fixtures and excluded.
set -uo pipefail

H="${HARNESS_DIR:-docs/harness}"
LOG="$H/DECISIONS.log"
FAILS=0

[[ -d "$H" ]] || { echo "audit-decisions: no $H — nothing to audit"; exit 0; }
[[ -f "$LOG" ]] || { echo "audit-decisions: ✗ $LOG missing while artifacts exist"; exit 1; }

require_line() {
  local pattern="$1" claim="$2"
  if grep -qE "$pattern" "$LOG"; then
    echo "  ✓ $claim"
  else
    echo "  ✗ UNLOGGED CLAIM: $claim (no DECISIONS.log line matching /$pattern/)"
    FAILS=$((FAILS+1))
  fi
}

echo "audit-decisions: cross-checking claims against $LOG"

# 1. STATE.md's "Last gate passed" claim
if [[ -f "$H/STATE.md" ]]; then
  GATE="$(sed -nE 's/.*Last gate passed \| *(G[0-9CE]+).*/\1/p' "$H/STATE.md" | head -1)"
  if [[ -n "$GATE" ]]; then
    require_line "$GATE passed" "STATE.md claims last gate passed = $GATE"
  else
    echo "  ~ STATE.md has no gate-passed claim (fresh or between items)"
  fi
fi

# 2. Change dossiers claiming GC ratification
for c in "$H"/changes/*/CHANGE.md; do
  [[ -e "$c" ]] || continue
  if grep -qE 'Status \|.*Ratified \(GC\)' "$c"; then
    ID="$(basename "$(dirname "$c")")"
    require_line "GC passed.*$ID" "change $ID claims Ratified (GC)"
  fi
done

# 3. Break-glass records must have their at-deploy log line
for b in "$H"/changes/*/BREAK-GLASS.md; do
  [[ -e "$b" ]] || continue
  ID="$(basename "$(dirname "$b")")"
  require_line "BREAK-GLASS \|.*$ID" "break-glass record $ID exists"
done

# 4. Release checklists claiming sign-off need a G7 line
if [[ -f "$H/RELEASE-CHECKLIST.md" ]] && grep -qE '^\| Version' "$H/RELEASE-CHECKLIST.md"; then
  require_line "G7 passed" "RELEASE-CHECKLIST.md exists (release claimed)"
fi

echo
if [[ $FAILS -gt 0 ]]; then
  echo "audit-decisions: FAIL ($FAILS unlogged claim(s)) — log them or retract the claims."
  exit 1
fi
echo "audit-decisions: all claims logged."
