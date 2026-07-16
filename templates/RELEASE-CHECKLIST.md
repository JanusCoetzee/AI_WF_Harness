# Release Checklist — <version>

| Field | Value |
| --- | --- |
| Version / git SHA | |
| Risk tier | |
| Release approver | |
| Change record # | <institutional change-management ticket> |
| Date | |

## Pre-release (all must be checked with evidence links)

- [ ] G4 evidence: verify loop green, log at `docs/harness/evidence/...`
- [ ] G5 evidence: human review record (reviewer names, tier-correct count)
- [ ] G6 evidence: secret scan, dep audit, threat-model delta, data sweep
- [ ] Eval scores ≥ ship floors for pinned model+prompt (AI features)
- [ ] Evidence bundle built: `scripts/evidence-bundle.sh <version>` — path: ______
- [ ] **Rollback rehearsed in pre-prod** — date + who ran it: ______
- [ ] DB migrations have a tested down-path OR "roll-forward only" ADR-### linked
- [ ] Dashboards & alerts live and receiving data (before traffic)
- [ ] Runbook updated; on-call briefed
- [ ] Abort thresholds defined: error rate ___, p95 ___, schema-failure rate ___ (AI)
- [ ] Change record approved (status, approver)
- [ ] Not a Friday / freeze window / market-sensitive date (T1)

## Rollout (T1: progressive; each promotion human-triggered)

| Step | Scope | Health check | Result | Promoted by |
| --- | --- | --- | --- | --- |
| Canary | | | | |
| Cohort | | | | |
| Full | | | | |

## Observation window

- Window: ___ (G7 passes at the END of this window, not at deploy)
- Signals watched:
- Anomalies & dispositions:

## Sign-off

Release approver: __________  Date: ______  → append to DECISIONS.log
