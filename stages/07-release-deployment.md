# Stage 07 — Release & Deployment

**Purpose:** Ship deliberately, observably, reversibly. Exit: **G7**.

## Sequence

1. **Evidence bundle** — `scripts/evidence-bundle.sh` snapshots PRD, PLAN, verify
   logs, eval scores, review record, G6 record into
   `docs/harness/evidence/<version>/` with checksums and the git SHA.
2. **Rollback rehearsal** — execute the rollback path in a pre-prod environment
   *before* the release, not after the incident. A rollback plan that has never run
   is a hypothesis. Data migrations need an explicit down-path or a documented
   "roll-forward only" decision (that's an ADR).
3. **Release checklist** — `templates/RELEASE-CHECKLIST.md` filled and committed.
4. **Progressive rollout** (T1): canary → cohort → full, with health checks and
   automatic or one-command halt at each step. Define the abort thresholds *before*
   starting (error rate, latency, eval-online metrics for AI features).
5. **Observation window** — dashboards and alerts live before traffic arrives.
   For AI features: online monitoring of output-schema failure rate, refusal rate,
   and drift against eval expectations.

## LLM role

- Draft the checklist, runbook (`templates/RUNBOOK.md`), rollout config, and
  dashboard/alert definitions.
- Drive the deployment scripts **only when a human explicitly triggers each
  environment promotion in-session**. Never auto-promote.
- During the observation window: watch signals, summarize honestly, recommend
  halt/continue — the halt decision is human on T1.

## Human role

- Release approver triggers each promotion and owns the halt/continue call.
- Confirms the change record is approved *before* the first production step.

## Anti-patterns

- Friday releases of T1 changes. The calendar is a control too.
- "The deploy is the test." Pre-prod parity gaps are findable at Milestone 0.
- Declaring success at deploy time. G7 passes at the *end* of the observation
  window, not when the pipeline turns green.
