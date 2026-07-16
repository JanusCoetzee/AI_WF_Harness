---
name: harness-ideate
description: Stage 00 — interrogate a raw idea into a falsifiable IDEA.md with kill criteria and a risk tier, targeting gate G0. Use when starting new work or triaging a hunch.
---

# harness-ideate

Playbook: `stages/00-ideation.md`. Template: `templates/IDEA.md`. Exit: G0.

1. Ask the user for the raw idea if not given. Then interrogate before drafting:
   who hurts today, how they cope, what it costs, why now. If the idea arrived as a
   solution ("build a dashboard"), force it back to the problem it implies.
2. Generate **three divergent framings** of the problem and present them briefly;
   let the user pick or blend before converging.
3. Write the **do-nothing steelman** honestly — most ideas in a bank should lose to it.
4. Propose **kill criteria** (observable, dated) and a **risk tier** with rationale
   using the tier questions in the template (money movement, data classification,
   regulatory surface, blast radius). Argue the tier properly — it sets all
   downstream ceremony.
5. Draft `docs/harness/IDEA.md`, update `STATE.md` (stage 00, tier, next gate G0).
6. Tell the user what G0 approval requires (`gates/GATES.md`): their sign-off, a
   sponsor if T1, and a `DECISIONS.log` line. You cannot approve it.
