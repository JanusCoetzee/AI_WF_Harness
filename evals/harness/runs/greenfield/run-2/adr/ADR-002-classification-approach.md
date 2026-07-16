# ADR-002 — Rules-first baseline with LLM assist, enabled per category in shadow

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-17 |
| Deciders | janus |
| REQs served | REQ-001, REQ-201, REQ-202 |

## Context

Six categories differ in structure: format failures and cutoff misses are fully
determined by status codes; sanctions near-miss and duplicate-suspect need judgment
over free text. Model risk appetite for T1 demands provable behavior per category.

## Options considered

### Option A — LLM classifies everything

- Pros: one path; handles ambiguity.
- Cons: pays model risk, latency, and eval burden for categories that are
  deterministic from status codes; injection surface for cases that never needed
  free text at all.

### Option B — deterministic rules where codes decide; LLM only for judgment categories; per-category shadow enablement

- Pros: ~60% of volume classified with zero model risk; LLM eval effort focuses on
  the two hard categories; each category flips from shadow to live only when its
  eval floor is met.
- Cons: two code paths; routing matrix must be owned by ops as configuration.

## Decision

Option B. Discriminating reason: don't spend model risk where a status code
already knows the answer.

## Consequences

Easier: per-category go/no-go with evidence. Harder: category ownership discipline.
Tripwire: if rules coverage drops below 50% of volume, revisit the split.
