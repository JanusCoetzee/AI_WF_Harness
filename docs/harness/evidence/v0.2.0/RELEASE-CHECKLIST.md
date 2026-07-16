# Release Checklist — v0.2.0 (CHG-001)

| Field | Value |
| --- | --- |
| Version / git SHA | v0.2.0 / (SHA of release commit, appended post-commit) |
| Risk tier | T2 |
| Release approver | janus (SIMULATED — e2e drill) |
| Change record # | none — no change system connected (drill gap, logged in secure-gate-record §6) |
| Date | 2026-07-17 |

## Pre-release

- [x] G4 evidence: verify green — `evidence/verify-20260717-090845.log` (9 tests)
- [x] G5 evidence: `review-record.md` (T2: 1 reviewer; SIMULATED, marked)
- [x] G6 evidence: `secure-gate-record.md` (scan clean-degraded, pip-audit clean, threat delta)
- [ ] Eval scores — N/A: no AI features in this change
- [x] Evidence bundle: `scripts/evidence-bundle.sh v0.2.0 --change CHG-001` → `evidence/v0.2.0/`
- [x] **Rollback rehearsed** — 2026-07-17, janus/AI pair: pre-change commit f0e7bd2 booted in a worktree on :5051, `/` 200, `/api/health` 404 (old behavior), torn down
- [x] DB migrations — none (code only)
- [ ] Dashboards & alerts — N/A for localhost tool; health endpoint IS the new observability
- [x] Runbook equivalent: README "Harness browser" section current
- [x] Abort thresholds: any non-200 from `/` or `/api/health` during observation → halt and revert
- [ ] Change record approved — SIMULATED (no system connected)
- [x] Not a freeze window (local tool)

## Rollout (T2: single step, human-triggered)

| Step | Scope | Health check | Result | Promoted by |
| --- | --- | --- | --- | --- |
| Restart :5050 with new code | full (single instance) | GET /api/health == 200 "ok" | (recorded below) | janus (SIMULATED) |

## Observation window

- Window: 10 consecutive checks post-restart (small tool ⇒ minutes, not days)
- Signals watched: HTTP codes on `/`, `/api/health`, `/api/catalog`; count stability
- Anomalies & dispositions: (recorded below)

## Sign-off

Release approver: janus (SIMULATED — e2e drill)  Date: 2026-07-17 → DECISIONS.log
