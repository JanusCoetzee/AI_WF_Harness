# ADR-001 — Real-time screening via VerifyChain API rather than accelerating the batch

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-17 |
| Deciders | janus + Head of Financial Crime Ops |
| REQs served | REQ-001, REQ-101 |

## Context

Screening latency must drop from up-to-24h to intake-time. The incumbent nightly
batch uses licensed lists in-house; VerifyChain offers a real-time API over
equivalent lists.

## Options considered

### Option A — accelerate the in-house batch to micro-batches (15 min)

- Pros: no new vendor; data stays in the estate.
- Cons: 15 minutes is still not intake-time; list-matching engine needs a rebuild
  for latency; misses the 90% unwind-reduction goal.

### Option B — VerifyChain real-time API at intake

- Pros: meets latency goal; matching engine maintained by a specialist; scores +
  evidence exceed the batch's output quality.
- Cons: PII crosses to a vendor; availability coupling on the payment path
  (mitigated by REQ-003 hold semantics); per-call cost.

### Option C — build an in-house real-time matching service

- Pros: data stays internal.
- Cons: a specialist matching engine is 6–9 months of build for a non-core
  competency; list-update latency becomes our problem forever.

## Decision

Option B. Discriminating reason: intake-time screening is the requirement, and
matching engines are a specialist product, not a differentiator to build.

## Consequences

Easier: latency goal reachable this quarter. Harder: vendor availability is now on
the payment path — REQ-003's hold queue carries that risk. Tripwire: hold-queue
p95 dwell over 60s at steady state forces a resilience redesign.
