#!/usr/bin/env bash
# evidence-bundle.sh — snapshot the audit trail for a release into
# docs/harness/evidence/<version>/ with checksums and git provenance.
# Usage: scripts/evidence-bundle.sh <version>
set -euo pipefail

VERSION="${1:?usage: evidence-bundle.sh <version>}"
H="${HARNESS_DIR:-docs/harness}"
OUT="$H/evidence/$VERSION"

mkdir -p "$OUT"

# Provenance
{
  echo "version:   $VERSION"
  echo "generated: $(date -u +%FT%TZ)"
  echo "git_sha:   $(git rev-parse HEAD 2>/dev/null || echo 'not-a-git-repo')"
  echo "git_state: $(git status --porcelain 2>/dev/null | wc -l | tr -d ' ') uncommitted paths"
  echo "generator: $(whoami)@$(hostname)"
} > "$OUT/PROVENANCE.txt"

# Core artifacts (warn-but-continue so the bundle shows the gaps honestly)
copy_if() {
  if [[ -e "$1" ]]; then
    cp -R "$1" "$OUT/"
    echo "  + $1"
  else
    echo "  ! MISSING: $1" | tee -a "$OUT/GAPS.txt"
  fi
}

echo "bundling evidence for $VERSION → $OUT"
copy_if "$H/IDEA.md"
copy_if "$H/PRD.md"
copy_if "$H/PLAN.md"
copy_if "$H/adr"
copy_if "$H/THREAT-MODEL.md"
copy_if "$H/EVAL-SPEC.md"
copy_if "$H/review-record.md"
copy_if "$H/secure-gate-record.md"
copy_if "$H/RELEASE-CHECKLIST.md"
copy_if "$H/DECISIONS.log"
# most recent verify log
LATEST_VERIFY="$(ls -t "$H"/evidence/verify-*.log 2>/dev/null | head -1 || true)"
[[ -n "$LATEST_VERIFY" ]] && { cp "$LATEST_VERIFY" "$OUT/"; echo "  + $LATEST_VERIFY"; } \
  || echo "  ! MISSING: verify log" | tee -a "$OUT/GAPS.txt"

# Checksums (tamper-evidence)
( cd "$OUT" && find . -type f ! -name SHA256SUMS -exec shasum -a 256 {} \; > SHA256SUMS )

echo
if [[ -s "$OUT/GAPS.txt" ]]; then
  echo "bundle built WITH GAPS — see $OUT/GAPS.txt. A gapped bundle cannot pass G7 for T1."
  exit 1
fi
echo "bundle complete: $OUT (commit it — the bundle is only evidence once it's in history)"
