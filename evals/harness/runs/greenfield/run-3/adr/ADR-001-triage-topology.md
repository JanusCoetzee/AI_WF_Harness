# ADR-001 — PayGuard consumes exceptions inline (synchronous shadow-then-live), not batch

| Field | Value |
| --- | --- |
| Status | Proposed |
| Date | 2026-08-12 |
| Deciders | Head of Payment Operations (business owner), Driver — pending G2 sign-off |
| REQs served | REQ-001, REQ-101, REQ-102 |

## Context

Exceptions arrive continuously on the Kafka topic (~1,100/day). REQ-101
requires classification not to add material latency (p95 < 5s), and REQ-102
requires the system to fail open to today's manual process rather than block
intake. The question: does PayGuard classify each exception as it arrives
(inline/streaming), or accumulate and classify in scheduled batches?

## Options considered

### Option A — Inline streaming consumer

- Sketch: a consumer group reads the Kafka topic continuously; each exception
  is classified as it arrives and the recommendation is written to the case
  tool before the analyst would normally pick it up.
- Pros: matches the existing continuous-arrival pattern; no artificial delay
  added ahead of the current 6-minute handle time; natural fit for REQ-101's
  per-exception latency bar.
- Cons: requires the consumer to be always-on and independently monitored;
  failure handling (REQ-102's fail-open) has to be designed per-message, not
  per-batch.
- Risks: a stuck/slow consumer could, without REQ-102's fail-open design,
  create a silent backlog invisible to analysts.

### Option B — Scheduled micro-batch (e.g. every 60s)

- Sketch: exceptions accumulate for a fixed window, classified together, then
  recommendations are pushed to the case tool.
- Pros: simpler operational model (batch job, not a long-running consumer);
  easier to reason about throughput and cost per run.
- Cons: adds up to 60s of latency ahead of the analyst's existing workflow for
  no benefit — the exception queue is already continuous, not batch-shaped,
  so batching is solving a problem this system doesn't have; complicates
  REQ-102's "degrades exactly to today's manual process" requirement, since a
  batch failure affects a whole window's worth of exceptions at once rather
  than degrading one at a time.
- Risks: batch-window failures are blast-radius-larger than per-message
  failures under Option A.

## Decision

Option A (inline streaming). The exception flow itself is continuous, not
batch-shaped, and REQ-101/REQ-102 are both stated per-exception, not
per-window — batching would import latency and larger failure blast radius to
solve a problem that doesn't exist here. AI pair recommends A; no
countervailing case for batching was found in the scenario facts.

## Consequences

Easier: per-exception fail-open (REQ-102) is a natural default (an unclassified
message just falls through to the existing manual queue, same as any message
processed before PayGuard existed). Harder: requires an always-on consumer
with its own health monitoring, not a schedulable job — ops must add this to
on-call/monitoring scope at G4. Tripwire: if sustained throughput materially
exceeds today's ~1,100/day and single-message processing can't keep pace,
revisit toward a hybrid (inline for the common path, batch backfill for
recovery after an outage).
