# ADR-001 — Triage runs as a sidecar recommender, not inside the hub consumer

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-17 |
| Deciders | janus (AI pair recommended Option B; human accepted for blast-radius reasons) |
| REQs served | REQ-001, REQ-002, REQ-006, REQ-102 |

## Context

Exceptions flow on a Kafka topic consumed by the ops case tool loader. Triage must
add recommendations without risking the ingestion path; gateway latency is variable.

## Options considered

### Option A — classify inline in the existing loader

- Sketch: loader calls gateway before writing the case.
- Pros: one deployable; no new topic.
- Cons: couples case ingestion to gateway health — an LLM outage delays case
  creation itself, violating "degradation never loses queue" (REQ-102). Widens the
  loader's data exposure to the redaction path.
- Risks: the worst failure mode (no cases at all) attaches to the least-owned code.

### Option B — sidecar service consuming the same topic, writing recommendations

- Sketch: `triage-svc` consumes hub events independently, writes recommendation
  records; case tool displays them; absence of a recommendation = manual queue.
- Pros: ingestion untouched; outage degrades to today's behavior; independent
  scaling; redaction confined to one service.
- Cons: second deployable; eventual consistency between case and recommendation.
- Risks: recommendation lag — bounded by REQ-101.

## Decision

Option B. The discriminating reason: failure isolation — an AI-path outage must
degrade to the status quo, never block case creation.

## Consequences

Easier: safe iteration on prompts/models. Harder: UI must handle "no recommendation
yet". Tripwire: if recommendation lag p95 exceeds 30s at peak, revisit.
