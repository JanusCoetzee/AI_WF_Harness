#!/usr/bin/env bash
# gate-check.sh — mechanical half of gate passage: asserts required evidence
# artifacts exist (and are non-trivially filled) before a gate can be approved.
# Human approval + DECISIONS.log entry are still required; this only checks (a).
# Usage: scripts/gate-check.sh G0|G1|G2|G3|G4|G5|G6|G7
#        scripts/gate-check.sh GC [CHG-###]   (brownfield fast path; defaults to newest change)
set -uo pipefail

H="${HARNESS_DIR:-docs/harness}"
GATE="${1:-}"
FAILS=0

need_file() {
  local f="$1" why="$2"
  if [[ ! -s "$f" ]]; then
    echo "  ✗ missing: $f  ($why)"; FAILS=$((FAILS+1))
  elif grep -qE 'CHANGE_ME|<work item name>|<name>|CHG-###' "$f"; then
    echo "  ✗ unfilled template: $f  ($why)"; FAILS=$((FAILS+1))
  else
    echo "  ✓ $f"
  fi
}

need_grep() {
  local pattern="$1" f="$2" why="$3"
  if [[ -s "$f" ]] && grep -qE "$pattern" "$f"; then
    echo "  ✓ $f contains /$pattern/"
  else
    echo "  ✗ $f lacks /$pattern/  ($why)"; FAILS=$((FAILS+1))
  fi
}

echo "gate-check $GATE (evidence dir: $H)"
case "$GATE" in
  GC)
    CHG="${2:-}"
    if [[ -z "$CHG" ]]; then
      CHG="$(ls -t "$H/changes" 2>/dev/null | head -1 || true)"
      [[ -z "$CHG" ]] && { echo "  ✗ no changes in $H/changes/ (run /harness-change first)"; exit 1; }
      echo "  (no change id given — checking newest: $CHG)"
    fi
    C="$H/changes/$CHG"
    need_file "$C/CHANGE.md" "one-page intake: intent, tier, acceptance, blast radius"
    need_grep 'T[123]' "$C/CHANGE.md" "risk tier must be assigned to the change"
    need_grep "$CHG\.[0-9]" "$C/CHANGE.md" "numbered acceptance criteria required"
    need_grep '[Bb]last radius' "$C/CHANGE.md" "blast-radius estimate required"
    need_grep '[Rr]ollback' "$C/CHANGE.md" "rollback note required"
    if grep -qi 'waived-trivial' "$C/CHANGE.md"; then
      echo "  ~ recon waived as trivial (waiver must state a reason in CHANGE.md)"
    else
      need_file "$C/RECON.md" "code map, consumers, implicit contracts, characterization tests"
      need_grep '[Gg]o' "$C/RECON.md" "go/no-go recommendation required"
    fi
    if grep -qE '\|[[:space:]]*[Yy]es[[:space:]]*\|' "$C/CHANGE.md"; then
      echo "  ✗ an escalation trigger is answered 'yes' — fast path exits to the full workflow"; FAILS=$((FAILS+1))
    else
      echo "  ✓ no escalation triggers tripped"
    fi
    ;;
  G0)
    need_file "$H/IDEA.md" "problem statement + kill criteria + tier"
    need_grep 'T[123]' "$H/IDEA.md" "risk tier must be assigned"
    need_grep '[Kk]ill criteria' "$H/IDEA.md" "kill criteria required"
    ;;
  G1)
    need_file "$H/PRD.md" "locked requirements"
    need_grep 'REQ-[0-9]{3}' "$H/PRD.md" "numbered requirements are the traceability spine"
    need_grep '[Nn]on-goals' "$H/PRD.md" "explicit non-goals required"
    ;;
  G2)
    ls "$H"/adr/ADR-*.md >/dev/null 2>&1 \
      && echo "  ✓ ADRs present: $(ls "$H"/adr/ADR-*.md | wc -l | tr -d ' ')" \
      || { echo "  ✗ no ADRs in $H/adr/"; FAILS=$((FAILS+1)); }
    need_file "$H/THREAT-MODEL.md" "per tier: full STRIDE or boundary table"
    ;;
  G3)
    need_file "$H/PLAN.md" "ratified milestone plan"
    need_grep 'M0' "$H/PLAN.md" "walking skeleton milestone required"
    need_grep '[Dd]emo command' "$H/PLAN.md" "every milestone needs a demo command"
    ;;
  G4)
    ls "$H"/evidence/verify-*.log >/dev/null 2>&1 \
      && echo "  ✓ verify log(s) present" \
      || { echo "  ✗ no verify logs in $H/evidence/ (run scripts/verify.sh --log)"; FAILS=$((FAILS+1)); }
    if grep -qi 'UNVERIFIED' "$H/STATE.md" 2>/dev/null && ! grep -qiE 'UNVERIFIED items.*none' "$H/STATE.md"; then
      echo "  ✗ STATE.md lists UNVERIFIED items"; FAILS=$((FAILS+1))
    else
      echo "  ✓ no outstanding UNVERIFIED items"
    fi
    ;;
  G5)
    need_file "$H/review-record.md" "human review record (names, tier-correct count)"
    ;;
  G6)
    need_file "$H/secure-gate-record.md" "secret scan / dep audit / threat delta / data sweep results"
    ;;
  G7)
    ls -d "$H"/evidence/*/ >/dev/null 2>&1 \
      && echo "  ✓ evidence bundle dir present" \
      || { echo "  ✗ no evidence bundle (run scripts/evidence-bundle.sh <version>)"; FAILS=$((FAILS+1)); }
    need_file "$H/RELEASE-CHECKLIST.md" "filled release checklist incl. rollback rehearsal"
    ;;
  *)
    echo "usage: $0 G0|G1|G2|G3|G4|G5|G6|G7 | GC [CHG-###]" >&2; exit 64 ;;
esac

echo
if [[ $FAILS -gt 0 ]]; then
  echo "gate-check $GATE: FAIL ($FAILS item(s) missing). Gate may not be approved."
  exit 1
fi
echo "gate-check $GATE: evidence PRESENT. Now obtain human approval and append to $H/DECISIONS.log."
