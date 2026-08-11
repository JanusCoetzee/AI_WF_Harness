# ADR-002 — Classify exceptions via the approved LLM gateway, not a bespoke ML classifier

| Field | Value |
| --- | --- |
| Status | Proposed |
| Date | 2026-08-12 |
| Deciders | Head of Payment Operations (business owner), Driver — pending G2 sign-off |
| REQs served | REQ-201, REQ-202 |

## Context

REQ-201/REQ-202 need exceptions classified into specialist routing queues
(in-scope types only) with a defined abstention behavior for low-confidence
and out-of-scope (sanctions-hold) cases. Two genuinely different technical
approaches exist for the classification step itself.

## Options considered

### Option A — LLM classification via the approved internal gateway

- Sketch: send the redacted exception (post REQ-203 masking) to the approved
  internal LLM gateway with a fixed prompt + schema-validated output
  (category + confidence + abstain flag); pin model version per EVAL-SPEC.md.
- Pros: fastest to stand up (no training pipeline); handles the free-text
  remittance-information signal the scenario flags as routinely containing
  routing-relevant context, without needing a labeled-feature-engineering
  cycle first; abstention (REQ-202) is a natural prompt/schema behavior.
- Cons: ongoing per-call cost at ~1,100/day volume; requires the full AI-behavior
  governance path (EVAL-SPEC.md, model risk registration, drift monitoring) that
  a simpler classifier might not.
- Risks: model drift over time (mitigated by EVAL-SPEC.md's regression policy
  and pinned model version).

### Option B — Purpose-trained ML classifier (e.g. gradient-boosted trees on structured fields + text features)

- Sketch: train a supervised classifier on historical exception → correct-queue
  labels using structured fields (status codes, amount, currency) plus
  engineered text features from remittance information.
- Pros: potentially cheaper per-call at volume; no LLM-specific governance
  overhead (no prompt-injection surface, since there's no natural-language
  instruction channel).
- Cons: requires a labeled historical dataset that isn't confirmed to exist
  yet (PRD's data inventory doesn't establish one); feature engineering on
  free-text remittance information is exactly the kind of unstructured-signal
  problem LLMs are suited for and bespoke feature pipelines are slower to
  iterate on; would still need its own eval/quality-bar discipline, just
  without a governance path this harness already has ready (EVAL-SPEC.md
  is written for AI behaviors generally, not LLM-specific, but the org's
  approved tooling — the internal LLM gateway — is the "no bespoke build"
  path called out favorably in the PRD's non-goals).
- Risks: unknown training-data availability is a real unknown, not a modeled
  one — if a labeled dataset doesn't exist, Option B's timeline risk is
  larger than stated here and would need its own discovery spike.

## Decision

Option A. The scenario's core signal (free-text remittance information) is
unstructured and the bank already has an approved, governed LLM gateway
in-estate — building a bespoke classifier would mean owning a training
pipeline and a labeled dataset whose existence isn't confirmed, for a problem
the approved tooling already fits. AI pair recommends A. Revisit Option B only
if per-call cost at scale (REQ-101 volume) becomes the binding constraint
after the shadow run proves the LLM approach's accuracy.

## Consequences

Easier: EVAL-SPEC.md's existing AI-behavior governance path (dataset,
scorers, thresholds, model risk registration) applies directly — no separate
ML-ops discipline to stand up. Harder: per-call cost scales with volume, and
this is now subject to the harness's full AI-behavior threat surface (see
THREAT-MODEL.md's AI-specific table) — prompt injection via remittance
free-text is a real, modeled threat, not hypothetical. Tripwire: if the
shadow run's accuracy (IDEA.md kill criterion, ≥75%) isn't met, or per-call
cost at production volume breaches budget, revisit toward Option B with a
proper discovery spike on labeled-data availability first.
