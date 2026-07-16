# Philosophy

Why this harness works the way it does. Read once; internalize; then live in the stage playbooks.

## 1. The LLM is a brilliant, forgetful contractor

An LLM pair is extraordinarily capable *within a well-framed task* and unreliable at
carrying context across days, sessions, or teams. Therefore:

- **Documents are the memory, not the chat.** PRDs, ADRs, plans, and `STATE.md` are the
  durable brain. Any decision that lives only in a conversation is a decision you will
  pay to rediscover.
- **Every session starts by reloading state**, not by trusting recollection.

## 2. Feedback loops beat intelligence (the Pocock axiom)

The quality of AI-assisted output is bounded by the quality and speed of the feedback
loop around it, not by the model. A model with `tsc --noEmit`, a lint wall, a fast test
suite, and evals will outperform a smarter model flying blind.

- Types and schemas turn "the model misunderstood" into a compile error in seconds.
- Runtime validation at boundaries (especially around *model output*) turns silent
  corruption into a loud failure.
- **Evals are tests for the probabilistic parts.** A prompt without an eval is a
  function without a test — worse, actually, because it regresses silently when the
  underlying model changes. Pin model versions; re-run evals before upgrading.

## 3. Momentum is a feature (the Tim axiom)

Long invisible stretches of work are where AI collaboration dies: context drifts, scope
creeps, and nobody can tell if you're 20% or 80% done.

- **Every milestone ends runnable.** "It compiles" is not a milestone; "you can run
  this command and see this behavior" is.
- Scaffold first. A walking skeleton (thin end-to-end slice) exposes integration risk
  in day one instead of week four.
- Demos are the honest progress report. If you can't demo it, it isn't done.

## 4. In a bank, the artifact *is* the work

In a regulated institution, undocumented working software is a liability, not an asset.
Auditors, model-risk teams, and future engineers need to reconstruct *why*, *who
approved*, and *what evidence existed at the time*.

- Gates convert "we're pretty sure" into checkable evidence in the repo.
- Traceability (`REQ-###` threading through commits, tests, ADRs) means any line of
  code can be defended in front of an auditor in minutes.
- Risk tiers keep this honest in both directions: a T1 payments change earns full
  ceremony; a T3 spike earns almost none. Uniform ceremony breeds ceremony-theater.

## 5. Segregation of duties applies to machines too

The AI drafts, critiques, and verifies — but it is structurally forbidden from
approving its own work, merging, or deploying. This is not distrust of the model; it is
the same control we apply to humans, and it is what makes AI-assisted delivery
*defensible* to a regulator rather than merely fast.

## 6. Design it twice, decide it once

For any non-trivial interface or architecture, have the LLM produce two or three
genuinely different shapes before committing (the `/design-an-interface` pattern).
Comparison is cheap at design time and ruinous after G3. Once decided, write the ADR
and stop relitigating — reopening a decision requires superseding the ADR, on purpose.
