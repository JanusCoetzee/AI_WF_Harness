---
name: harness-retro
description: Stage 08 — run the retro that closes the loop; audit gate performance and AI-pairing patterns, and propose harness improvements. Use after a release or fortnightly.
---

# harness-retro

Playbook: `stages/08-operate-learn.md`. Template: `templates/RETRO.md`.

1. Gather evidence before opinions: walk the PRD's REQ list against what shipped;
   pull the DECISIONS.log timeline; list incidents/anomalies from the observation
   window; diff estimated vs. actual milestones from PLAN.md's change log.
2. **Gate audit**: for each gate passed this cycle — what did it catch, what
   slipped through that it *should* have caught? Propose specific adjustments to
   `gates/GATES.md`, not vibes.
3. **AI-pairing audit** — be candid about yourself: where did the pairing shine,
   where did it burn time (thrash loops, invented APIs, scope drift, verbose
   detours)? Each burn pattern becomes a proposed rule change to `CLAUDE.md`;
   each shine pattern gets kept deliberately.
4. **Ceremony audit**: name at least one harness ceremony that produced no value
   this cycle and propose trimming it. A harness that only grows becomes the
   bureaucracy it replaced.
5. Draft `docs/harness/RETRO-<date>.md` with actions (owner + due date — untracked
   actions are audit findings) and the feed-forward list for the next Stage 00.
6. Offer to apply the agreed `CLAUDE.md`/gate changes in the same session — the
   harness is versioned and improved like code.
