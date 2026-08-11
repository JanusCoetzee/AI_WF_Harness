# PRD — PayGuard: automated payment-exception triage & routing

| Field | Value |
| --- | --- |
| Status | Draft |
| Risk tier | T1 (from IDEA.md — Confidential data, sanctions-timeline regulatory surface, re-confirmed here) |
| Business owner | Head of Payment Operations |
| Driver | AI pair (blind-run production, evals/harness) |
| Last updated | 2026-08-12 |

## Problem

14 payment-operations analysts manually triage ~1,100 exceptions/day (format
failures, sanctions near-miss holds, insufficient-funds returns, suspected
duplicates, cutoff misses) at ~6 minutes average handle time. ~30% of routed
cases bounce to the wrong specialist team. SLA breaches are up ~8% QoQ; two
analysts have resigned citing workload. The smallest testable version scopes
the first shadow run to the two highest-volume, lowest-compliance-risk
exception types (format failures, cutoff misses), explicitly excluding
sanctions-hold cases from any automated routing until accuracy is proven.

## Goals & success measures

- Reduce first-pass misrouting (bounce rate) on in-scope exception types from
  ~30% to ≤10% within one quarter of shadow-run start.
- Reduce average handle time on in-scope exception types by ≥20% within one
  quarter of live routing (post-shadow), without an increase in re-bounce rate.
- Zero sanctions-hold cases auto-routed during the scoped rollout (analysts
  remain the sole router for that exception type until a separate, later REQ
  set is approved).

## Non-goals

- No auto-resolution of payment exceptions — routing only; the analyst who
  receives a case still owns the outcome.
- No automated routing of sanctions-hold cases in this scope (see IDEA.md
  do-nothing/kill criteria — a future PRD revision, not this one, would cover it).
- No change to the payments hub, the Kafka topic contract, or the ops case
  tool's data model — PayGuard consumes and annotates, it does not own
  upstream systems.
- No public model API usage — the approved internal LLM gateway only (see
  REQ-104).

## Requirements

### Functional

| ID | Requirement | Acceptance criteria (testable) | Source |
| --- | --- | --- | --- |
| REQ-001 | Consume payment exceptions from the internal Kafka topic and classify each into a specialist routing queue | Given an exception event on the topic, when classified, then the case is annotated with a routing recommendation and the original event is unmodified | Scenario brief — payments hub integration |
| REQ-002 | Route in-scope exception types (format failures, cutoff misses) to the recommended queue after analyst confirmation | Given a routing recommendation, when an analyst confirms it in the case tool, then the case moves to the recommended queue and the confirmation is logged with actor + timestamp | Scenario brief — ops case tool routing |
| REQ-003 | Exclude sanctions-hold exceptions from automated routing recommendations entirely | Given an exception classified as sanctions-hold, when processed, then no routing recommendation is generated and the case is flagged for manual handling per existing process | IDEA.md — do-nothing/kill criteria scope exclusion |
| REQ-004 | Every routing decision (recommended or analyst-overridden) is attributable and reconstructable | Given any routed case, when queried later, then the record shows classification input, model recommendation, analyst action, and timestamps | Regulatory & reporting impact (below) |

### Non-functional

| ID | Requirement | Acceptance criteria | Source |
| --- | --- | --- | --- |
| REQ-101 | Performance: classification must not add material queue latency | p95 classification latency < 5s per exception at the current ~1,100/day sustained volume | Derived — must not become the new bottleneck given 6-min current handle time |
| REQ-102 | Availability: classification unavailability degrades to the current manual process, never blocks intake | Given the classification service is down, when an exception arrives, then it queues for manual triage exactly as it does today (fail-open on availability, not on control — see REQ-004/REQ-203 for the separate fail-closed rule on Confidential-data handling) | Derived — the exception queue must never stall on this system |
| REQ-103 | Auditability: every state change attributable to an actor + timestamp | Given any system-driven or analyst state change on a case, then actor + timestamp are recorded and queryable | Template baseline, reinforced by REQ-004 |
| REQ-104 | All model calls route through the approved internal LLM gateway, EU region, no direct public model API calls | Given any classification call, when inspected, then the call target is the approved gateway endpoint only | Scenario brief — data-residency constraint |

### AI-behavior requirements

| ID | Behavior | Quality bar (links to EVAL-SPEC) | Human-in-loop? |
| --- | --- | --- | --- |
| REQ-201 | Classify exception into correct specialist queue (in-scope types only) | eval `payguard-routing-accuracy` ≥ 75% suggestion accuracy on shadow-run data (matches IDEA.md kill criterion) | Yes — analyst confirms every routing decision before the case leaves the queue (REQ-002); no auto-resolution ever |
| REQ-202 | Refuse/abstain (route to manual queue) rather than guess on low-confidence or out-of-scope (sanctions-hold) cases | eval `payguard-routing-accuracy` — abstention correctness ≥ 95% on sanctions-hold-shaped inputs in test set | Yes — abstained cases fall to today's manual process, no new human step introduced |
| REQ-203 | Remittance free-text is redacted/masked before any content reaches the LLM gateway prompt | eval `payguard-redaction` — 100% of test-set customer names/account numbers/invoice details redacted pre-prompt | N/A (pre-prompt control, not a per-case human step) |

## Regulatory & reporting impact

Mandatory in a regulated institution — "none" is a finding to justify, not a default.

| Question | Answer |
| --- | --- |
| Which regulations/timelines does this touch (payments, sanctions, reporting, resilience)? | Sanctions-hold handling timelines (mitigated by REQ-003's total exclusion of that exception type from automated routing in this scope) |
| Does any figure produced here feed regulatory, tax, or financial reporting? | No — routing recommendations are operational, not a reported figure. Handle-time/bounce-rate metrics (Goals section) are internal operational KPIs only |
| What audit trail must exist for automated or AI-influenced decisions? | Per REQ-004: classification input, model recommendation, analyst action, actor + timestamp, retained per the bank's standard case-record retention policy (owner: Payment Operations — exact retention period is an open question below) |
| Does this change what a customer sees or receives (statements, notices)? | No — routing is an internal ops-tool change only; no customer-facing artifact changes |

## Reconciliation & control totals

Every exception event consumed from the Kafka topic must be accounted for
exactly once in the case tool — no exception silently dropped by the
classification step, no exception double-routed. Control: a daily count
reconciliation between (a) exceptions consumed off the topic and (b) cases
present in the ops case tool for that day, with any delta raised as a break.
Owned by REQ-004 (auditability) and REQ-101/102 (fail-open-to-manual on
unavailability ensures no exception is silently lost rather than queued).

## Third parties

N/A — the classification service calls the bank's own approved internal LLM
gateway (already an approved, in-estate control per the scenario brief), not
an external vendor. No new third party is introduced by this PRD; if a future
revision introduces an external classification/NLP vendor, this section
becomes mandatory at that time.

## Data inventory

| Element | Classification | Source of truth | Retention | Enters prompts? |
| --- | --- | --- | --- | --- |
| Payment reference, amount, currency, status codes | Internal | Payments hub (Kafka topic) | Per existing case-tool retention policy | Yes — structural fields, not PII |
| Counterparty details | Confidential | Payments hub (Kafka topic) | Per existing case-tool retention policy | Only in redacted/tokenized form (REQ-203) |
| Remittance free-text (customer names, account numbers, invoice details) | Confidential | Payments hub (Kafka topic) | Per existing case-tool retention policy | Only after redaction/masking (REQ-203) — raw text never enters a prompt |
| Routing recommendation + analyst action log | Internal | PayGuard (system of record for this feature) | Owner to confirm — see Open Questions | No — output artifact, not prompt input |

## Open questions

| # | Question | Owner | Resolved in (REQ/ADR) |
| --- | --- | --- | --- |
| — | none outstanding | — | — |

All questions raised during drafting were resolved before lock: exact
audit-log retention period defaults to the bank's standard case-record
retention policy (Data inventory, above) pending confirmation from the
business owner at G1 sign-off — treated as a resolved default, not an open
REQ-attached question, per gates/GATES.md G1 ("Fails if... any REQ-### has an
open question attached in PRD.md at approval time", ADR-004).

## Ruling log

| Conflict | Resolution |
| --- | --- |
| Ops leadership's initial ask ("an AI thing that sorts the queue") implied full auto-resolution | Scoped down to routing-with-confirmation only (REQ-002) — no REQ requires or permits auto-resolution; analysts stay accountable for outcomes per the scenario's own restated ask |
| Whether sanctions-hold cases should be in scope for the first release | Excluded entirely (REQ-003) given T1 tier and regulatory-timeline blast radius (IDEA.md risk tier proposal) — revisit only after the in-scope shadow run proves accuracy |
