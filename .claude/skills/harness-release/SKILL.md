---
name: harness-release
description: Stage 07 — evidence bundle, rollback rehearsal, release checklist, and human-triggered progressive rollout, targeting gate G7.
---

# harness-release

Playbook: `stages/07-release-deployment.md`. Template: `RELEASE-CHECKLIST.md`. Exit: G7.

Precondition: G6 in `DECISIONS.log`. Hard rule: **you never trigger a promotion —
each environment step is a human action in-session.**

1. Build the evidence bundle: `scripts/evidence-bundle.sh <version>`. A bundle with
   GAPS.txt cannot pass G7 on T1 — surface gaps as the headline.
2. Fill `docs/harness/RELEASE-CHECKLIST.md`. Do not tick what hasn't happened;
   an unticked box with a reason beats a hopeful tick.
3. **Rollback rehearsal**: draft the exact procedure, have the human run it in
   pre-prod, record date + operator in the checklist. Untested rollback = G7 fail.
   DB migrations need a tested down-path or a "roll-forward only" ADR.
4. Define **abort thresholds before rollout starts**: error rate, p95, and for AI
   features schema-failure rate / refusal rate. Write them in the checklist.
5. Draft rollout config (canary → cohort → full for T1), dashboards, alerts, and
   the runbook (`templates/RUNBOOK.md`) — all live before traffic.
6. During the observation window: watch the signals, summarize honestly,
   recommend halt/continue. The halt decision is human on T1. G7 passes at the
   **end of the window**, not when the pipeline goes green.
7. On pass: `DECISIONS.log` line, STATE.md → stage 08, suggest `/harness-retro`.
