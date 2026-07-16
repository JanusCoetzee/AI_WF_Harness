# ISSUE — <behavior-shaped title: what a user/system can do when this closes>

The ticket is the prompt. It must pass the **fresh-session test**: an engineer or LLM
with only this ticket and repo access can do the work with no archaeology, no tribal
knowledge, no "ask around".

## Context — why this exists

Two or three sentences: the problem this slice solves and where it fits. Links do the
heavy lifting:

- Requirement(s): REQ-### / CHG-### (or this ticket's own key on the fast path)
- Design constraints: ADR-### <one-line summary of the constraint, inline>
- Parent plan / milestone: PLAN.md M_
- Depends on: <ticket keys, or "nothing — independently shippable">

## Vertical slice — layers this cuts through

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

| # | Given / When / Then |
| --- | --- |
| 1 | |
| 2 | |

## Proof — how done is demonstrated

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
- [ ] Vertical slice table filled — or horizontal exception justified
- [ ] Acceptance criteria testable as written
- [ ] Proof command stated
- [ ] Out-of-scope stated
- [ ] Sized ≤ ~1 day; if bigger, split before creating, not after starting
