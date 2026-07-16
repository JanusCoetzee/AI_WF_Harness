# Stage 04 — Implementation

**Purpose:** Execute the plan in small verified steps, milestone by milestone. Exit: **G4**.

This is where the harness earns its keep. The loop per task:

```text
pick task → write/extend the failing test → implement → scripts/verify.sh → commit (REQ-### in message) → update PLAN.md
```

## LLM role

- **Schema/type first, then test, then code.** New boundaries get their contract
  before their implementation; LLM outputs get runtime validation, never a cast.
- Run the **verify loop after every change** (`scripts/verify.sh`). Report failures
  verbatim; never summarize a red run as "mostly passing".
- Keep steps small enough that a red verify has one plausible cause.
- Commit messages: imperative summary + `REQ-###` + what was verified.
- At each milestone end: run the **demo command**, paste the observed output into
  `PLAN.md`, update `STATE.md`.
- When stuck twice on the same failure: stop, state hypotheses, instrument — don't
  thrash. Three failed attempts = escalate to the human with a written diagnosis.
- For AI features: every prompt edit re-runs the eval suite. Score deltas go in the
  commit message. A prompt "improvement" that drops a score is a regression.

## Human role

- Unblock, decide, and spot-check diffs as they land — not in one 3,000-line lump later.
- Guard scope: new ideas go to the PRD/PLAN as proposals, not into the branch.
- Pass G4 when verify is green, demos are recorded, and nothing is `UNVERIFIED`.

## Testing rules

- Test behavior via public interfaces; don't handcuff refactoring to internals.
- Changed lines need covering tests; deleted tests need a written reason.
- Synthetic fixtures only — a production record in a fixture is a G6 failure waiting.
- Flaky test = broken test. Fix or quarantine with a ticket, never retry-until-green.

## Anti-patterns

- "I'll run the tests at the end." The end is where debugging goes to die.
- Letting the LLM weaken an assertion to make a test pass. Watch for this in review;
  it is the single most common failure mode of AI pairing.
- Big-bang integration after weeks of parallel pieces — that's what Milestone 0 was for.
