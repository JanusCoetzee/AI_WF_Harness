# PRD — <work item name>

| Field | Value |
| --- | --- |
| Status | Draft / **Locked (G1)** |
| Risk tier | T1 / T2 / T3 (from IDEA.md, re-confirmed here) |
| Business owner | |
| Driver | |
| Last updated | YYYY-MM-DD |

## Problem

One paragraph. Who hurts, how they cope today, why now. (Lift from IDEA.md, sharpened.)

## Goals & success measures

Observable, dated measures. "Reduce manual reconciliation effort by X hours/week within one quarter of launch."

## Non-goals

The explicit list of things this work will NOT do. Each entry prevents a future argument.

## Requirements

Every requirement: numbered, testable as written, with a named source.

### Functional

| ID | Requirement | Acceptance criteria (testable) | Source |
| --- | --- | --- | --- |
| REQ-001 | | Given / When / Then | |
| REQ-002 | | | |

### Non-functional

| ID | Requirement | Acceptance criteria | Source |
| --- | --- | --- | --- |
| REQ-101 | Performance: | p95 < ___ms at ___ rps sustained ___ min | |
| REQ-102 | Availability: | | |
| REQ-103 | Auditability: | Every state change attributable to an actor + timestamp | |

### AI-behavior requirements (delete section if no AI features)

| ID | Behavior | Quality bar (links to EVAL-SPEC) | Human-in-loop? |
| --- | --- | --- | --- |
| REQ-201 | | eval `<name>` ≥ <threshold> | per tier |

## Regulatory & reporting impact

Mandatory in a regulated institution — "none" is a finding to justify, not a default.

| Question | Answer |
| --- | --- |
| Which regulations/timelines does this touch (payments, sanctions, reporting, resilience)? | |
| Does any figure produced here feed regulatory, tax, or financial reporting? | |
| What audit trail must exist for automated or AI-influenced decisions? | |
| Does this change what a customer sees or receives (statements, notices)? | |

## Reconciliation & control totals

For anything that moves, transforms, or counts records of value: how do we prove
nothing was lost or double-processed between systems? Name the control (counts,
hash totals, break reports) and the REQ that owns it.

## Data inventory

Every data element touched. Anything above `Internal` cannot enter prompts without a logged exception.

| Element | Classification | Source of truth | Retention | Enters prompts? |
| --- | --- | --- | --- | --- |

## Open questions

| # | Question | Owner | Resolved in (REQ/ADR) |
| --- | --- | --- | --- |

## Ruling log

Conflicts between stakeholders and their resolutions. The PRD records the ruling; chat does not count.
