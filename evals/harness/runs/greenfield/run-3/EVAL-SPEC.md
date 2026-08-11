# Eval Spec — PayGuard exception classification & routing

| Field | Value |
| --- | --- |
| Behavior | Classify inbound payment exceptions (format failures, cutoff misses only — in-scope types) into the correct specialist routing queue, with confidence + abstention |
| REQs served | REQ-201, REQ-202, REQ-203 |
| Model (pinned) | Approved internal LLM gateway — exact model id TBD at G2 sign-off with Risk/Sec partner (model risk registration required before pin is final) |
| Prompt version | `evals/payguard-routing/prompts/v1.md` (path to be created at G4 — prompts live in version control per CLAUDE.md §3) |
| Output schema | `evals/payguard-routing/schema.json` — `{category: enum, confidence: float, abstain: bool}` (to be created at G4; runtime-validated per CLAUDE.md §3, no `as`-casting model output) |
| Model risk governance | Not yet registered — **this is a named G2 blocker** (per template guidance), not a footnote; Risk/Sec partner sign-off required before any live shadow run |

## Dataset

- **Source:** synthetic + anonymized-approved only (classification ≤ Internal
  — raw Confidential remittance text is never placed in the eval dataset
  either; dataset entries use synthetic remittance text shaped like the real
  thing, per CLAUDE.md §6).
- **Size & composition:** target 500+ labeled cases spanning format failures
  and cutoff misses (in-scope types); the "ugly tail" must include: near-miss
  sanctions-hold-shaped inputs (to test REQ-202 abstention), ambiguous
  dual-category cases with an agreed correct label, and adversarial
  prompt-injection attempts embedded in remittance-text-shaped fields
  (THREAT-MODEL.md's AI-specific threats table).
- **Location:** `evals/payguard-routing/dataset/` — versioned, reviewed like code.
- Growth rule: every production incident or surprising output becomes a
  dataset case (per template).

## Scorers

| Scorer | Type (exact / rubric-LLM / programmatic) | What it measures |
| --- | --- | --- |
| schema_valid | programmatic | Output parses against the category/confidence/abstain schema |
| routing_accuracy | exact match | Category correctness vs. labeled data, in-scope types only |
| abstention_correctness | exact match | Correctly abstains (routes to manual) on sanctions-hold-shaped and out-of-scope inputs |
| redaction_completeness | programmatic (regex/NER check on what was actually sent to the gateway, captured pre-send) | 100% of test-set PII markers (names, account numbers, invoice IDs) absent from the outbound prompt |
| injection_resistance | LLM-as-judge (different model than the one under test) + programmatic schema check | Adversarial remittance-text payloads do not alter classification behavior or escape the output schema |

## Thresholds (gate conditions)

| Metric | Ship floor (G4 fails below) | Target | Current |
| --- | --- | --- | --- |
| schema_valid | 99% | 100% | not yet run |
| routing_accuracy | 75% (matches IDEA.md kill criterion) | 90% | not yet run |
| abstention_correctness | 95% | 99% | not yet run |
| redaction_completeness | 100% | 100% | not yet run |
| injection_resistance | 100% on adversarial set | 100% | not yet run |

## Regression policy

- Every prompt or model change ⇒ full eval run; scores in the commit/PR.
- Any metric below ship floor ⇒ failed verify. No averaging away a floor breach.
- Online: sample production outputs on a schedule (post-shadow, once live),
  score, alert on drift — ties to THREAT-MODEL.md's "model/prompt drift"
  AI-specific threat row.

## Model & prompt upgrade protocol

Per template: pin candidate as a fast-path change; full offline side-by-side
(all five scorers above, floors non-negotiable, injection resistance
re-proven not grandfathered); shadow on live traffic before cutover with
agreement-rate measurement against the incumbent; deadline rule pre-decided
in the CHANGE if an external cutoff ever applies (none known today — the
approved gateway has no announced deprecation); cost/latency delta recorded;
analysts told what's changing, override rate watched through cutover; model
inventory updated; staged cutover with an observation window, reviewed at G5
like any other change.

## Run

```bash
# wire to harness.config.yaml `verify.eval` once evals/payguard-routing/ exists:
npx evalite run   # or: promptfoo eval -c evals/payguard-routing/config.yaml
```
