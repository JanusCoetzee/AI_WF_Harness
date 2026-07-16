---
name: harness-review
description: Stage 05 — adversarial AI self-review plus reviewer pack preparation for human review, targeting gate G5. Use when a milestone or work item is ready for review.
---

# harness-review

Playbook: `stages/05-review.md`. Exit: G5 (human-approved; your review is input only).

Precondition: G4 evidence exists (`scripts/gate-check.sh G4`).

1. **Adversarial self-review** of the full diff — hunt for reasons to FAIL it:
   - Plausible-but-wrong: boundaries, off-by-one, rounding modes, timezone math.
   - Test theater: tests that exercise mocks instead of behavior; weakened asserts.
   - Invented APIs: calls that don't exist in the pinned dependency versions —
     check the lockfile, don't trust memory.
   - Unvalidated boundaries: any external or LLM data crossing without its schema.
   - REQ drift: diff hunks serving no REQ (silent scope), REQs with no tests.
   - Standards breaches (`docs/STANDARDS.md`): thresholds the tools measure are
     verify's job, but the `manual (G5)` rows — contract-first API changes,
     schema-validated AI boundaries — are checked here, explicitly.
   - Rank findings by severity, each with a concrete failure scenario. No praise
     padding — zero findings means say "no findings above <bar>", not compliments.
2. **Traceability spot-check**: pick 3 REQs at random, walk each to code + tests +
   acceptance criteria. Report any break.
3. **Reviewer pack** (`docs/harness/review-record.md`, top section): what changed
   and why, REQs served, verify/eval evidence links, demo instructions, trade-offs,
   and **your areas of least confidence** — that's where human minutes should go.
4. If the diff exceeds ~500 changed lines, recommend splitting before human review.
5. Remind: G5 needs tier-correct human approvals (T1=2, T2=1), recorded in the
   review record + `DECISIONS.log`. Your approval counts for nothing.
