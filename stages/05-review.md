# Stage 05 — Review & Verification

**Purpose:** Independent human judgment on work the AI helped produce. Exit: **G5**.

## Sequence

1. **AI adversarial self-review first.** The LLM reviews its own diff *hunting for
   reasons to fail it*: correctness bugs, weakened tests, unvalidated boundaries,
   REQ drift, hallucinated APIs. Output attached to the PR as reviewer *input*.
2. **Human review second**, calibrated by tier (T1 = 2 reviewers, T2 = 1).
3. **Traceability spot-check:** pick 3 REQs at random; walk each to its code, tests,
   and acceptance criteria. Any break fails the gate.

## LLM role

- Produce the adversarial self-review (`/harness-review` runs this) — findings ranked
  by severity, each with a concrete failure scenario, no praise padding.
- Prepare the reviewer pack: what changed and why, REQs served, verify/eval evidence,
  demo instructions, known trade-offs, areas of least confidence. **Declare where you
  are least confident** — that's where humans should spend their minutes.
- Apply review feedback in small verified commits; never force-push over a review.

## Human role

- Review with special attention to the AI failure modes that human-written code
  rarely has:
  - **Plausible-but-wrong**: code that reads beautifully and is subtly incorrect
    (off-by-one on boundaries, wrong rounding mode, timezone assumptions).
  - **Test theater**: tests that exercise the mock, not the behavior.
  - **Invented APIs**: calls to methods/flags that don't exist in the pinned version.
  - **Silent scope**: helpful extras nobody asked for (delete them; they're untested REQ-less liability).
- Enforce the PR size ceiling (~500 changed lines per review sitting). Bigger = split.
- Record the review outcome in `docs/harness/` and pass G5.

## Anti-patterns

- Treating a clean AI self-review as a reason to skim the human review. The self-review
  finds what the model can see; the human is there for what it can't.
- Review comments resolved in chat instead of in the code or the PRD.
