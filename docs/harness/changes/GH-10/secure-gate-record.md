# Secure Gate Record — #10 (G6)

| Field | Value |
| --- | --- |
| Change | #10 — doctrine API + authz interface (commits `e38c19d` build, `71be594` G5 fix, `35bbed8` CI fix) |
| Tier | T2 — Driver walks checklist; no Risk/Sec partner required |
| Date | 2026-08-18 |

## 1. Secret scan — PASS, with a disclosed residual

Two runs, not one, to be honest about scope:

- **The pipeline as actually configured** (`gitleaks-action`, push-triggered,
  scans only the new push's commit(s)): clean on `35bbed8` — confirmed live,
  `gh run view 32088937018` both jobs green.
- **A true full-history scan** (`gitleaks detect`, no `--log-opts` limit, 40
  commits): still reports 1 finding — `71be594e...:docs/harness/changes/
  GH-10/review-record.md:generic-api-key:55`. This is the same confirmed
  false positive investigated and logged earlier today (`DECISIONS.log`):
  plain traceability-table prose, no credential present. It was fixed
  **forward** (an inline `gitleaks:allow` marker in the current file
  content, `35bbed8`), not by rewriting `71be594`'s already-pushed history.
  A full-history rescan still sees `71be594`'s own diff without that
  marker — this is the honest shape of "fixed forward," not a new finding.
  **Not treated as a blocker**: the actual CI gate (push-scoped) is clean,
  the underlying content was verified not to be a secret before any
  suppression, and rewriting pushed `main` history is a decision for the
  Driver, not something to do unasked to make a report look cleaner.

## 2. Dependency audit — PASS

`pip-audit -r app/requirements.txt` (flask 3.1.3, markdown 3.10.2,
gunicorn 23.0.0, bleach 6.4.0, **PyYAML 6.0.3** — new in `#10`, for the
`doctrine:` config pin): **"No known vulnerabilities found."** STD-004
satisfied — no High/Critical, no waivers needed.

## 3. Threat-model delta — PASS

Full delta appended to `docs/harness/changes/GH-8/THREAT-MODEL.md` (§"Delta
review — #10"), not summarized-and-lost here. Highlights:

- Flagship threat (prompt injection via retrieved docs): **verified**, not
  just designed — fail-closed integrity (`test_10_2_*`) and explicit-
  version-only (`test_10_3_*`, structurally no versionless route) are both
  shipped and tested.
- RBAC-at-retrieval (ADR-002 amendment): **verified live** at G5, not just
  by unit test — `is_allowed()` fail-closed, manifest listing itself
  filtered, not just gated fetches.
- **Assumption #1 (real SSO) is still open** — `#10` ships a documented
  stub only, by design (out of scope per its own ticket). Restated in the
  threat model as a **G7 deployment blocker**, not a `#10` gap, so it
  doesn't quietly get treated as satisfied between now and actual deploy.
- Named, not backfilled: `#9`'s own G6/threat-model delta was never done —
  flagged in `THREAT-MODEL.md`'s header row rather than silently left.

## 4. Data-handling sweep — PASS

`scripts/data-scan.sh` (ADR-007, verify.sh's own lint step) — clean. Manual
check on `#10`'s new content specifically: test fixtures in
`tests/test_doctrine_api.py` use only synthetic paths/content ("original
content", "tampered content", throwaway `tmp_path` repos) — no real account
numbers, emails, or credentials. The doctrine content `#10` actually serves
(the harness's own docs/gates/templates) was already Internal-max under the
existing browser (`#9`'s G5) — `#10` adds no new data classification, it
adds enforcement of the ceiling that was previously implicit.

## 5. AI-feature checks — N/A

No LLM calls in `#10`'s code path (confirmed by threat-model delta's
"Denial of wallet: N/A" row) — service serves and gates access to
documents, doesn't generate or interpret them.

## 6. Change record — real ticket, not simulated

Unlike `CHG-001`'s drill-era G6 record, this repo now has real
ticketing: `#10` itself (GitHub issue) is the change-management record
CLAUDE.md §5 requires ("the ticket is the prompt"). No separate
`CHG-###` needed — `#10`'s key is the traceability ID throughout
`PLAN.md`, `DECISIONS.log`, and this file.

## Verdict

**PASS** at T2. No waivers needed — the one disclosed residual (full-
history gitleaks finding) is a confirmed false positive already
investigated and logged, not a policy exception requiring
`expiry_date`/`owner` under `harness.config.yaml`'s waiver rules.

**Driver verdict:** Approve. janus, 2026-08-18, in-session (`DECISIONS.log`).
