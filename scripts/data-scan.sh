#!/usr/bin/env bash
# data-scan.sh — verify-time pattern scan for hardcoded secrets and PII-shaped
# strings (ADR-007, Option C). Chained into the `lint` step of the verify loop
# so it runs on every verify, not on every keystroke (Option A, a real-time
# PreToolUse hook, was considered and declined — this repo has additional
# guardrails behind the scenes that catch serious PII violations; this scan
# is a lightweight second net over what lands in the harness's own tree).
# Escape hatch: a `# data-scan: allow` comment on the offending line.
# Exit 1 = pattern found, exit 0 = clean.
set -uo pipefail

FAILS=0

# git-tracked + untracked-but-not-ignored files; skip obvious binary/lock noise.
FILES="$(git ls-files --cached --others --exclude-standard 2>/dev/null \
  | grep -vE '\.(png|jpg|jpeg|gif|ico|pdf|lock)$|(^|/)\.venv/|(^|/)node_modules/')"

[[ -z "$FILES" ]] && { echo "data-scan: no files to scan"; exit 0; }

PATTERNS=(
  'AKIA[0-9A-Z]{16}'                                          # AWS access key id
  '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----'            # PEM private key
  '[Aa][Pp][Ii]_?[Kk][Ee][Yy][[:space:]]*[:=][[:space:]]*[\"'"'"'][A-Za-z0-9_\-]{16,}[\"'"'"']'  # api_key = "..."
  '[Pp]assword[[:space:]]*[:=][[:space:]]*[\"'"'"'][^\"'"'"']{6,}[\"'"'"']'                        # password = "..."
  '\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'                              # SSN-shaped
  '\b([0-9]{4}[- ]){3}[0-9]{4}\b'                               # card-number-shaped
)

for pattern in "${PATTERNS[@]}"; do
  while IFS= read -r hit; do
    [[ -z "$hit" ]] && continue
    file="${hit%%:*}"
    line="${hit#*:}"
    if printf '%s' "$line" | grep -q 'data-scan: allow'; then
      continue
    fi
    echo "  ✗ $hit"
    FAILS=$((FAILS+1))
  done < <(printf '%s\n' "$FILES" | xargs -I{} grep -nE "$pattern" {} 2>/dev/null)
done

if [[ $FAILS -gt 0 ]]; then
  echo "data-scan: ✗ $FAILS potential secret/PII pattern(s) found (CLAUDE.md §6)." >&2
  echo "Fix the finding, or if genuinely a false positive add '# data-scan: allow' on that line." >&2
  exit 1
fi

echo "data-scan: ✓ clean"
