---
name: harness-build
description: Stage 04 — execute the ratified plan task-by-task with schema-first, test-first, verify-after-every-change discipline, targeting gate G4. Use to start or resume implementation.
---

# harness-build

Playbook: `stages/04-implementation.md`. Exit: G4.

Precondition: G3 in `DECISIONS.log`. Resume from `STATE.md` current task.

The loop, per task:

1. **Pick** the next unchecked task in the active milestone (announce it + its REQ).
2. **Contract first** if the task creates a boundary: schema/type before code.
   LLM output gets runtime validation — never a cast.
3. **Test first**: write or extend the failing test (name references the REQ).
4. **Implement** the smallest change that makes it pass.
5. **Verify**: run `scripts/verify.sh`. Red output gets reported verbatim — never
   summarize a red run as "mostly passing". If verification is impossible, mark the
   change `UNVERIFIED` in STATE.md and say so out loud.
6. **Commit** when instructed: imperative summary + `REQ-###` + what was verified.
7. **Update** PLAN.md checkbox and STATE.md.

Milestone end: run the **demo command**, paste observed output into PLAN.md's demo
record (G4 evidence), update STATE.md, and show the user the demo.

Circuit breakers:

- Same failure twice → stop, write hypotheses, instrument. Three failures →
  escalate to the human with a written diagnosis. No thrashing.
- New idea mid-build → PLAN.md "Out-of-plan proposals" table, not the branch.
- Never weaken an assertion to get green. If a test seems wrong, say so and ask.
- Eval score drops after a prompt change = regression, even if the output "looks better".
