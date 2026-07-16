---
name: harness-plan
description: Stage 03 — decompose approved design into a milestone plan where every milestone ends runnable and demoable, targeting gate G3.
---

# harness-plan

Playbook: `stages/03-planning.md`. Template: `templates/PLAN.md`. Exit: G3.

Precondition: G1 (and G2 where tier requires it) in `DECISIONS.log`.

1. Draft `docs/harness/PLAN.md`:
   - **M0 is always the walking skeleton**: repo scaffold, CI, the thinnest
     end-to-end slice of the real flow, deployable to a lower environment.
     Integration risk dies at M0, not in week four.
   - Every milestone is a **behavior with a demo command** and expected
     observation — never a component name.
   - Tasks ≤ half a day each, every task mapped to a `REQ-###`. If a task resists
     decomposition, flag it: the design isn't understood yet.
   - Test strategy per milestone: unit/integration split, which evals stay green.
2. Sequence **riskiest-assumption-first**, not easiest-first. Say explicitly which
   assumption each early milestone kills.
3. If the plan exceeds ~2 weeks, insert a re-planning checkpoint.
4. Present the milestone map for the user to reshape — the human owns the
   sequencing bet. Then update `STATE.md`.
5. State G3 needs: run `scripts/gate-check.sh G3`, human ratification,
   `DECISIONS.log` line.
