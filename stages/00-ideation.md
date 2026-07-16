# Stage 00 — Ideation

**Purpose:** Turn a hunch into a falsifiable idea worth spending discovery time on. Exit: **G0**.

## Inputs

A problem, an irritation, a retro action, or a business ask.

## LLM role

- Interrogate the idea, don't decorate it. Ask: who hurts today, how do they cope now,
  what changes if this exists, what is the smallest version that tests the premise?
- Generate 3 divergent framings of the problem before converging (cheap at this stage).
- Steelman the "do nothing" option — in a bank, most ideas lose to "do nothing" and should.
- Draft `IDEA.md` and propose a **risk tier** with rationale (money movement? customer
  data? regulatory surface?). Tier drives all downstream ceremony, so argue it properly.

## Human role

- Provide the real context the model can't know: politics, adjacent systems, prior failures.
- Decide the kill criteria — the observable conditions under which this idea dies.
- Approve tier and G0, or kill it now (killing at G0 is a success, not a failure).

## Outputs

- `docs/harness/IDEA.md` — problem statement, affected users, why now, smallest
  testable version, kill criteria, proposed risk tier + rationale.
- `STATE.md` initialized with stage/tier.

## Anti-patterns

- Ideas that arrive as solutions ("build a dashboard") — force them back to the problem.
- Skipping tier assignment because "it's obviously small." Tier creep is how a T3 spike
  ends up processing production payments.
