# PRD — Real-time sanctions screening at payment intake

| Field | Value |
| --- | --- |
| Status | Locked (G1) — drill |
| Risk tier | T1 — sanctions control on money movement |
| Business owner | Head of Financial Crime Ops |
| Driver | janus |
| Last updated | 2026-07-17 |

## Problem

Counterparty screening runs as a nightly batch; payments accepted during the day are
screened up to 24h later, creating exposure and manual unwind work on late matches.

## Goals & success measures

- Screening decision available at intake: p95 < 500ms end-to-end within one quarter.
- Late-match unwind cases reduced ≥ 90% vs. batch-only baseline.

## Non-goals

- No change to match-adjudication workflows (analysts keep the same case tool).
- No replacement of list management; VerifyChain consumes the lists we already license.
- No screening of non-payment flows (onboarding uses its own path) this quarter.

## Requirements

### Functional

| ID | Requirement | Acceptance criteria (testable) | Source |
| --- | --- | --- | --- |
| REQ-001 | Screen counterparty at intake via VerifyChain API | Given a payment, when intake runs, then a screening result (clear / match-candidate) attaches before release | FinCrime ops |
| REQ-002 | Match candidates route to the analyst case tool with score + evidence | Given a candidate, when routed, then the case carries vendor score and matched-list entry | FinCrime ops |
| REQ-003 | On VerifyChain timeout or unavailability, the payment is **held in the screening queue** until a screening result exists; intake never releases without one | Given vendor timeout, when intake runs, then the payment holds with reason code and retries per policy | FinCrime ops |
| REQ-004 | Every screening decision has an audit trail: request fields, vendor response id, score, disposition, actor, timestamps — attributable to actor + timestamp, retained 7y | Given any released payment, when audited, then its screening chain reconstructs | Compliance |

### Non-functional

| ID | Requirement | Acceptance criteria | Source |
| --- | --- | --- | --- |
| REQ-101 | Vendor call p95 ≤ 300ms; end-to-end screening p95 ≤ 500ms at 40 rps | load test evidence | Platform |
| REQ-102 | Vendor SLA 99.9%; hold-queue drain alarms at 5 min depth | | Ops |

## Regulatory & reporting impact

| Question | Answer |
| --- | --- |
| Regulations/timelines touched | Sanctions regimes; screening timeliness expectations |
| Figures feeding regulatory/tax/financial reporting | No — case volumes feed internal MI only |
| Audit trail for automated decisions | REQ-004 |
| Customer-visible change | Payment release timing improves; no document changes |

## Reconciliation & control totals

Every intake payment must have exactly one screening outcome: intake count =
cleared + candidates + held, break report to ops hourly. Owned by REQ-005.

| ID | Requirement | Acceptance criteria | Source |
| --- | --- | --- | --- |
| REQ-005 | Screening pipeline control total | Given an hour's traffic, when the control job runs, then counts balance and breaks page ops | Compliance |

## Data inventory

| Element | Classification | Source of truth | Retention | Enters prompts? |
| --- | --- | --- | --- | --- |
| Counterparty name, address fragments | Confidential (PII) | payments hub | 7y | n/a — no LLM in flow |
| Bank identifiers (BIC/account) | Confidential | payments hub | 7y | n/a |
| Vendor response (score, list entry) | Confidential | VerifyChain response | 7y | n/a |

## Open questions

| # | Question | Owner | Resolved in |
| --- | --- | --- | --- |
| 1 | Retry policy depth for held payments before manual escalation | FinCrime ops | REQ-003 criteria |
