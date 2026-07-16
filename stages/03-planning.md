# Stage 03 — Planning

**Purpose:** Decompose the design into milestones an LLM pair can execute without drift. Exit: **G3**.

## Inputs

`PRD.md`, ADRs, `THREAT-MODEL.md` (per tier).

## LLM role

- Draft `PLAN.md` from `templates/PLAN.md`:
  - **Milestone 0 is always the walking skeleton** — the thinnest end-to-end slice
    that touches every layer (repo scaffold, CI, deploy-to-nowhere, hello-world of
    the real flow). Integration risk dies here, not in week four.
  - Every milestone ends **runnable and demoable** with a stated demo command and
    expected observation.
  - Tasks ≤ half a day. If you can't decompose it, you don't understand it yet —
    say so and go back to the design.
  - Map every task to its `REQ-###`. Unmapped work is scope creep with a head start.
  - State the test strategy per milestone: what gets unit tests, what gets
    integration tests, which evals must stay green.
- Sequence for **feedback, not dependency elegance**: riskiest-assumption-first.

- **Externalize the plan as tickets** (`/harness-issues`): each task or coherent
  cluster becomes a Jira/GitHub issue built from `templates/ISSUE.md` — one vertical
  slice per issue, self-contained enough to pass the fresh-session test, Definition
  of Ready checked before creation. The ticket is the prompt: every downstream stage
  inherits its quality, so it must be correct at birth. Write ticket keys back into
  PLAN.md's task rows; from then on the ticket key is the traceability handle.

## Human role

- Ratify or reshape the plan; the human owns the sequencing bet.
- Approve the drafted issues before they're created — tickets are shared, outward
  artifacts.
- Set the re-planning checkpoint (any plan > 2 weeks gets one).
- Pass G3.

## Outputs

- `docs/harness/PLAN.md` — milestones, tasks, demo commands, REQ mapping, test strategy.

## Anti-patterns

- Milestones named after components ("build the parser") instead of behaviors
  ("`harness demo m2` parses the sample file and prints totals").
- A plan that front-loads all the easy work — momentum theater.
- Treating the plan as immutable. Plans are updated deliberately (logged), not silently.
