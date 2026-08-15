# IDEA — Understanding checkpoint (stage-agnostic drift detection)

| Field | Value |
| --- | --- |
| Status | Draft |
| Driver | janus |
| Sponsor (T1 only) | N/A — not T1 |
| Date | 2026-08-12 |
| Constitution sections consulted | §9 (ambiguous requirement → check the PRD first, then ask — this idea generalizes that principle to "checkpoint understanding," not just resolve ambiguity when it's already surfaced), §4 (milestones — smallest testable version below is deliberately a walking skeleton, not a new skill/command) |

## Problem statement

Gates (G0 sign-off, G1 lock, G5 review, ...) already force a restate-and-confirm
moment between the Driver and the AI, and `harness-ideate`'s own step 2 ("three
divergent framings... let the user pick or blend") does this specifically at
Stage 00. But gates are coarse — once per stage, sometimes days apart on a real
work item — so the AI's understanding of what the Driver actually means can
drift silently *between* gates, on anything long or complex spanning several
sources of truth (docs, prior ADRs, stated constraints, existing code). Nothing
today catches that drift until a downstream artifact is already built on the
wrong premise, and the cost of catching it late is redoing whatever was built
on top of the wrong understanding, not just the misunderstanding itself.

This surfaced from the Driver's own Masters coursework exposing them to formal
reconciliation tools (a literature-review "synthesis matrix") and prompting the
question of whether the harness's existing, purely narrative reconciliation
(three framings, PRD ruling log) is enough once a work item gets long enough
for drift to compound between gates.

## Why now

The harness has just been through several long, multi-stage sessions in a row
(#8's build slices, the GH-12–23 backlog) where understanding was established
once and then carried across many turns and even across cold-context sessions
(GH-16, GH-17–23's blind runs) without an intermediate re-confirmation step.
Those happened to land correctly (independently re-verified each time), but
that was checked *after the fact*, expensively, by a human/second-session
audit — not caught cheaply, in-flight, by design.

## Smallest testable version

Not a new skill, command, or template. Document the move itself — restate
current understanding as a short table (source/input → understood as →
confidence), Driver corrects inline — as a named, invocable pattern in
`docs/harness/OPERATING-PROTOCOL.md`. Try it informally on one real upcoming
work item with genuine multi-source complexity (#10 doctrine API + authz is
the natural candidate — it has to reconcile ADR-002's original contracts,
ADR-008's per-BU amendment, and GH-21's newly-proposed classification field).
If it catches a real drift, or the Driver finds themselves reaching for it
unprompted, that's the signal to formalize further (dedicated command,
required-at-milestone-boundaries, etc.). If it doesn't get used or doesn't
catch anything a gate wouldn't have caught anyway, that's the kill signal.

## Kill criteria

- If, after being tried on #10 (or the next work item of comparable
  multi-source complexity), the Driver reports it added friction without ever
  catching a real drift that a gate wouldn't have caught anyway — kill it.
- If informally asking "restate your understanding" (no harness ceremony at
  all) turns out to be sufficient on its own within that same trial — don't
  formalize further; the do-nothing case wins and this stays undocumented.
- If it's invoked and ignored (Driver stops bothering to correct the table)
  more than once — the format is wrong or the timing is wrong; revise or kill
  before extending it.

## Do-nothing steelman

Every gate already forces a restate-and-confirm moment, and Stage 00 already
has one built in. The Driver can already ask "restate your understanding of
X" at any point, informally, at zero cost and with zero new harness
machinery — nothing prevents that today. The case *for* formalizing it is
narrow: gates are infrequent relative to how much drift can accumulate on a
long work item, and a named, documented move is something any session
(especially a cold one) knows to reach for or proactively offer, where an
informal habit depends entirely on the Driver remembering to ask. That's a
real but modest edge, not an obvious win — most of this idea's value is
genuinely uncertain until tried once on real work, which is exactly why the
smallest testable version above is documentation-only, not a built feature.

## Risk tier proposal

| Question | Answer |
| --- | --- |
| Moves money or affects customer outcomes? | No |
| Touches data above Internal? | No — process/documentation change only |
| Regulatory / reporting surface? | No |
| Blast radius if wrong? | Low per-instance (one extra restate-and-correct exchange, ignorable if unhelpful), but it changes `OPERATING-PROTOCOL.md`, which every future session reads — a badly-specified version could add friction across every subsequent work item, not just this one, until corrected |
| **Proposed tier + rationale** | T2 — no money/data/regulatory surface (would be T3 on those grounds alone), but the blast radius sits in the *operating protocol itself*, which is why this isn't going straight to a doc edit: it earns the same ceremony ADR-003 through ADR-009 got for exactly this reason (changes to how the harness governs everything else) |
