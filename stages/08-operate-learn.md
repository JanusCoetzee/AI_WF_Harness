# Stage 08 — Operate & Learn

**Purpose:** Run what you shipped, and feed what you learned back into the loop.

## Operating

- The runbook (`templates/RUNBOOK.md`) is live documentation: every incident that
  finds it wrong fixes it in the same PR as the remediation.
- Alerts page on symptoms users feel, not on internal mechanics. Every alert has a
  runbook entry; an alert without a next action is noise and gets deleted.
- **AI features in production:**
  - Track output-schema failure rate, refusal rate, latency, and cost per call.
  - Sample outputs on a schedule and score them against the eval suite — drift is
    silent and *will* happen (model updates, input distribution shifts).
  - A proposed model or prompt change re-enters the workflow at Stage 04 with an
    eval run; it is a change like any other.

## Incidents

- Stabilize first, diagnose second, document third — but all three, always.
- Blameless post-incident review within a week; actions get owners and dates and are
  tracked to closure (in a bank, an untracked incident action is an audit finding).
- The LLM drafts the timeline from logs/chat and proposes contributing factors; the
  humans judge causation.

## Retro (the loop-closer)

After each release (or fortnightly, whichever is sooner) run `/harness-retro`:

- What did the gates catch? What slipped through — and which gate *should* have
  caught it?
- Where did the LLM pairing shine, and where did it burn time (thrash loops,
  invented APIs, scope drift)? Update `CLAUDE.md` rules with what you learned —
  **the harness itself is versioned and improved like code.**
- Which ceremony produced no value this cycle? Propose trimming it. A harness that
  only ever grows becomes the bureaucracy it was built to replace.

Retro outputs feed Stage 00 of the next cycle. That's the whole point.
