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


# 5. DECISIONS.log's own internal chronology (GH-19): dates must be
# non-decreasing down the file. A misdated/out-of-order entry undermines the
# log's whole point of being a trustworthy, ordered audit trail.
echo
echo "audit-decisions: checking $LOG chronology"
PREV=""
PREV_LINE=""
LINENO=0
while IFS= read -r line; do
  LINENO=$((LINENO+1))
  [[ "$line" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})\  ]] || continue
  DATE="${BASH_REMATCH[1]}"
  if [[ -n "$PREV" && "$DATE" < "$PREV" ]]; then
    echo "  ✗ OUT OF ORDER: $LOG:$LINENO dated $DATE comes after a $PREV entry"
    echo "      prior: $PREV_LINE"
    echo "      this:  $line"
    FAILS=$((FAILS+1))
  fi
  PREV="$DATE"
  PREV_LINE="$line"
done < "$LOG"
[[ $FAILS -eq 0 ]] && echo "  ✓ $LOG dates are non-decreasing"

# 6. "#<n> closed"-shaped claims vs actual GitHub issue state (GH-20).
# Best-effort: skip with a warning (not a failure) if gh isn't available or
# authenticated — this check needs network access CI/offline dev may lack.
echo
echo "audit-decisions: checking closed-issue claims against GitHub"
if ! command -v gh >/dev/null 2>&1 || ! gh auth status >/dev/null 2>&1; then
  echo "  ~ skipped: gh not installed/authenticated (best-effort check, not enforced)"
else
  CLAIMED_CLOSED="$(grep -ohE '(#|GH-)[0-9]+ closed' "$LOG" "$H/STATE.md" 2>/dev/null | grep -oE '[0-9]+' | sort -un)"
  for n in $CLAIMED_CLOSED; do
    STATE="$(gh issue view "$n" --json state -q .state 2>/dev/null)"
    if [[ -z "$STATE" ]]; then
      echo "  ~ #$n: could not fetch issue state (skipped)"
    elif [[ "$STATE" != "CLOSED" ]]; then
      echo "  ✗ #$n claimed closed in $LOG/STATE.md but GitHub reports $STATE"
      FAILS=$((FAILS+1))
    else
      echo "  ✓ #$n confirmed CLOSED on GitHub"
    fi
  done
  [[ -z "$CLAIMED_CLOSED" ]] && echo "  ~ no '#<n> closed' claims found"
fi

echo
if [[ $FAILS -gt 0 ]]; then
  echo "audit-decisions: FAIL ($FAILS unlogged/inconsistent claim(s)) — log them or retract the claims."
  exit 1
fi
echo "audit-decisions: all claims logged."
