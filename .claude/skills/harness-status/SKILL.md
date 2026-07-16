---
name: harness-status
description: Report or initialize the AI Workflow Harness state — current stage, risk tier, next gate and its missing evidence. Use at session start or whenever unsure where the work item stands.
---

# harness-status

1. Read `docs/harness/STATE.md`. If missing, this project hasn't been initialized:
   - Create `docs/harness/` (plus `adr/` and `evidence/` subdirs).
   - Copy `templates/STATE.md` into it; create an empty `DECISIONS.log`.
   - Tell the user the next step is `/harness-ideate`.
2. If present, cross-check STATE.md against reality — don't just read it back:
   - Does the last-gate-passed claim have a matching `DECISIONS.log` line?
   - Run `scripts/gate-check.sh <next-gate>` and list exactly what evidence is missing.
   - If STATE.md contradicts the artifacts on disk (e.g. claims G3 but no PLAN.md),
     report the discrepancy as the headline, not a footnote.
3. Output a compact status block: work item, tier, stage, last gate (with log line),
   next gate + missing evidence, active milestone/task, blockers, UNVERIFIED items.
4. End with the single most useful next action (one sentence, one command).
