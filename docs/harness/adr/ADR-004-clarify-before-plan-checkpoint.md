# ADR-004 — Requirement ambiguity is a G1 failing condition, not a new stage

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-25 |
| Deciders | janus (Driver) |
| REQs served | N/A — harness process improvement, not tied to a work-item REQ/CHG |

## Context

A comparison against `github/spec-kit` surfaced its `/speckit.clarify` step: an
explicit checkpoint between spec drafting and planning where the agent forces
iterative dialogue until the spec is unambiguous, before `/plan` proceeds.

This harness's Stage 01 Discovery already describes similar intent —
"rewrite every requirement until it is testable as written" — but nothing
requires it as a checkable gate condition; it's guidance an author can satisfy
loosely and still pass G1. If we don't decide anything here, ambiguous
requirements can silently reach architecture (G2), where the cost of
re-litigating them is higher.

## Options considered

### Option A — Standalone `/harness-clarify` step between Discovery and Architecture

- Sketch: new skill/stage inserted after `01-discovery.md`, before
  `02-architecture.md`; produces a checklist of open questions in `PRD.md`
  that must reach zero before G1 is claimed passed.
- Pros: makes the "requirements must be unambiguous" requirement a checkable
  gate condition instead of an implicit expectation; matches spec-kit's
  explicit `/speckit.clarify` step; highly visible as a named checkpoint.
- Cons: a new stage number/file for what Stage 01 arguably already owns;
  more ceremony for small PRDs where ambiguity was never a real risk.
- Risks: becomes a rubber-stamp checklist if not tied to a real gate
  condition — a named step without teeth is worse than no step.

### Option B — Fold into existing G1 evidence requirement, no new stage

- Sketch: add one line to `gates/GATES.md` G1 "Fails if" row: "any REQ has an
  open question attached in PRD.md at approval time." No new file, no new
  slash command — `harness-prd` already produces `PRD.md`; this just makes an
  implicit expectation an explicit, checkable gate failure condition.
- Pros: zero new ceremony; reuses the existing artifact and existing gate;
  consistent with "standards are failing conditions, not review feedback"
  (`CLAUDE.md` §2).
- Cons: less visible than a named step; relies on `harness-prd`'s author to
  actually track open questions in the document rather than a dedicated
  workflow forcing it.
- Risks: none materially beyond Option A's rubber-stamp risk.

## Decision

**Option B.** Fold into G1's existing "Fails if" evidence — no new stage. The
gap identified was enforcement, not a missing step: Stage 01 already
describes the right behavior ("rewrite every requirement until testable"); it
just isn't a checkable gate failure condition yet. Add to `gates/GATES.md`
under G1 "Fails if": an unresolved open question attached to any REQ at
approval time fails the gate.

AI recommendation: Option B — the same "strengthen an existing gate over
inventing a new stage" reasoning applied across this whole comparison. A new
named stage is worth it only if Stage 01 turns out not to own this in
practice; that's a signal to watch for, not assume in advance.

## Consequences

**Easier:** ambiguous requirements can no longer silently pass G1; the fix is
a one-line addition to an existing gate's fail condition, not a new
process to learn or maintain.

**Harder / new commitments:** `harness-prd` authors must now actively track
open questions inside `PRD.md` rather than resolving them in conversation and
moving on — a discipline change more than a process change.

**Tripwire to revisit this ADR:** if G1 keeps passing with requirements that
turn out ambiguous at G2 despite this fail condition, that's the signal Stage
01 needs a real standalone clarify checkpoint (Option A) rather than a gate
condition nobody is checking rigorously.
