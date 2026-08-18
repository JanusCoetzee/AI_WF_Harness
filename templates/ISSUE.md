# ISSUE — <behavior-shaped title: what a user/system can do when this closes>

The ticket is the prompt. It must pass the **fresh-session test**: an engineer or LLM
with only this ticket and repo access can do the work with no archaeology, no tribal
knowledge, no "ask around".

**Mid-build finding shortcut (ADR-014):** if this ticket exists *only* because ADR-014
requires one before fixing a significant or platform-level bug found while building
something else — not a planned feature, not its own discrete task — collapse the body
to three lines instead of the full shape below:

> **What's broken:** \
> **Why it's significant** (the platform/architecture-level reason a routine
> in-service fix wouldn't need a ticket for — new config, new dependency, altered
> behavior of a shared mechanism): \
> **What "fixed" looks like:**

Skip the Vertical slice table, the formal acceptance-criteria table, and Proof —
state them inline in "What fixed looks like" only if the fix genuinely needs more than
a sentence. Context's Depends-on/Linked-records, Out-of-scope, Verify, and the
Definition of Ready still apply; this is a lighter *body*, not a different *ticket*.
A routine build-time correction made in service of an already-ticketed piece of work
doesn't need any of this — ADR-014 doesn't require a ticket for those at all.

## Context — why this exists

Two or three sentences: the problem this slice solves and where it fits. Links do the
heavy lifting:

- Requirement(s): REQ-### / CHG-### (or this ticket's own key on the fast path)
- Design constraints: ADR-### <one-line summary of the constraint, inline>
- Parent plan / milestone: PLAN.md M_
- Depends on: <ticket keys, or "nothing — independently shippable">
- Linked records: <audit findings, incidents, regulatory items — or "none checked">

## Vertical slice — layers this cuts through

*(Skip for a mid-build finding ticket using the shortcut above.)*

Name every layer; a ticket that touches one layer is a horizontal task wearing a
ticket costume (rare exceptions: pure refactor, dependency bump — say so explicitly).

| Layer | What changes here |
| --- | --- |
| UI (React/Flask view) | |
| API contract | <schema first — link or inline the shape> |
| Backend (Spring Boot/Python) | |
| Data | |
| Deploy/config | |

## Acceptance criteria — testable as written

*(Skip for a mid-build finding ticket — "What fixed looks like" above covers it.)*

| # | Given / When / Then |
| --- | --- |
| 1 | |
| 2 | |

## Proof — how done is demonstrated

*(Skip for a mid-build finding ticket, unless the fix needs a real demo to trust.)*

Demo command (or manual steps) + expected observation. This becomes the PLAN.md demo
record / PR evidence.

```bash
<command>
# expect: <observation>
```

## Out of scope

What an eager implementer might reasonably include but must not. Each line here
prevents a scope argument in review.

## Verify

Standard loop (`scripts/verify.sh`) plus anything slice-specific: which test files
are expected to grow, which evals must stay green, integration check across the
backend/frontend boundary if the slice crosses it.

---

### Definition of Ready (creator checks before the ticket is born)

- [ ] Title is a behavior, not a component
- [ ] Passes the fresh-session test (complete brief, links resolve)
- [ ] Vertical slice table filled — or horizontal exception justified (or the
      mid-build finding shortcut used instead — ADR-014)
- [ ] Acceptance criteria testable as written (or "What fixed looks like" stated,
      mid-build shortcut)
- [ ] Proof command stated (or judged genuinely unneeded, mid-build shortcut)
- [ ] Out-of-scope stated
- [ ] Sized ≤ ~1 day; if bigger, split before creating, not after starting
