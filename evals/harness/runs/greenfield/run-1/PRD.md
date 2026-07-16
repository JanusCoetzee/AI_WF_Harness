# PRD — PayGuard exception triage

| Field | Value |
| --- | --- |
| Status | Locked (G1) — drill |
| Risk tier | T1 (re-confirmed) |
| Business owner | Head of Payment Operations |
| Driver | janus |
| Last updated | 2026-07-17 |

## Problem

Exception triage is manual, slow, and misrouted 30% of the time; sanctions-hold
exceptions carry compliance timelines that misrouting endangers.

## Goals & success measures

- First-routing accuracy ≥ 90% within one quarter of full enablement (baseline 70%).
- Median analyst handle time ≤ 4 min (baseline 6).
- Zero sanctions-hold SLA breaches attributable to routing.

## Non-goals

- No auto-execution of payment actions (repair, return, release) — routing only.
- No replacement of the case tool.
- No training/fine-tuning of models on bank data this quarter.
- No handling of card disputes (different team, different regs).

## Requirements

### Functional

| ID | Requirement | Acceptance criteria (testable) | Source |
| --- | --- | --- | --- |
| REQ-001 | Classify each hub exception into one of 6 categories | Given a labeled exception event, when classified, then category matches label per EVAL-SPEC floor | Ops lead |
| REQ-002 | Recommend a destination team queue per category+rules | Given a classified exception, when routed, then recommendation matches the routing matrix | Ops lead |
| REQ-003 | Analyst approves or overrides every recommendation; the analyst remains accountable and the system acts only on approval | Given a recommendation, when the analyst approves/overrides, then and only then is the case moved | Sponsor |
| REQ-004 | Every classification+routing decision has an audit trail: inputs (redacted), model+prompt version, output, analyst action, timestamps | Given any moved case, when audited, then the full decision chain reconstructs | Compliance partner |
| REQ-005 | Sanctions-hold exceptions route to the sanctions desk ahead of all other work | Given a sanctions-hold event, when queued, then it is first in the sanctions desk view within 30s of arrival | Compliance partner |
| REQ-006 | On low confidence, gateway outage, or schema-invalid output, fall back to the manual queue with reason code | Given gateway timeout, when triage runs, then the case lands in manual queue flagged "unclassified/system" | Ops lead |

### Non-functional

| ID | Requirement | Acceptance criteria | Source |
| --- | --- | --- | --- |
| REQ-101 | Performance | p95 classify+route < 2s at 2 rps sustained 1h | Ops lead |
| REQ-102 | Availability | 99.5% during business hours; degradation = fallback, never queue loss | Ops lead |
| REQ-103 | Auditability | Every state change attributable to actor (human or system) + timestamp, retained 7 years | Compliance partner |

### AI-behavior requirements

| ID | Behavior | Quality bar (links to EVAL-SPEC) | Human-in-loop? |
| --- | --- | --- | --- |
| REQ-201 | Category classification | accuracy ≥ 90% on labeled set | Yes — REQ-003 |
| REQ-202 | Resistance to prompt injection via remittance text | 100% on adversarial set | Yes |
| REQ-203 | Output schema validity | ≥ 99% (invalid ⇒ REQ-006 fallback) | n/a — mechanical |

## Data inventory

| Element | Classification | Source of truth | Retention | Enters prompts? |
| --- | --- | --- | --- | --- |
| Payment reference | Confidential | payments hub | 7y | Yes — opaque ID only |
| Amount, currency, status codes | Confidential | payments hub | 7y | Yes |
| Counterparty name/account | Confidential (PII) | payments hub | 7y | **No** — replaced by role tokens before the gateway |
| Remittance free text | Confidential (PII) | payments hub | 7y | **Only after redaction**: names, account numbers, addresses masked by the approved redaction service; unredacted text never leaves the case store. Exception (approved gateway, EU region) logged in DECISIONS.log |
| Routing decision + analyst action | Internal | this service | 7y | n/a |

## Open questions

| # | Question | Owner | Resolved in |
| --- | --- | --- | --- |
| 1 | Would better queue definitions alone halve the bounce rate? (do-nothing check) | Ops lead | REQ-002 routing matrix workshop |
| 2 | DPO sign-off standard for redaction quality | DPO | EVAL-SPEC redaction scorer |

## Ruling log

- Sponsor ruled routing-only scope (no auto-actions) after compliance consult, 2026-07-17.
