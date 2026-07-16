# Eval Spec — <AI behavior name>

A prompt without an eval is a function without a test — and it regresses silently when
the model changes. Thresholds are agreed at G2, **before** the prompt exists.

| Field | Value |
| --- | --- |
| Behavior | <e.g. "classify inbound payment exceptions into 6 categories"> |
| REQs served | REQ-2## |
| Model (pinned) | <exact model id> |
| Prompt version | <path in repo — prompts live in version control> |
| Output schema | <path to Zod/JSON Schema/pydantic — runtime-validated> |

## Dataset

- **Source:** synthetic + anonymized-approved only (classification ≤ Internal).
- **Size & composition:** ___ cases; include the ugly tail — edge cases, adversarial
  inputs (injection attempts), ambiguous cases with agreed "correct" handling.
- **Location:** `evals/<behavior>/dataset/` — versioned, reviewed like code.
- Growth rule: every production incident or surprising output becomes a dataset case.

## Scorers

| Scorer | Type (exact / rubric-LLM / programmatic) | What it measures |
| --- | --- | --- |
| schema_valid | programmatic | Output parses against schema (should be ~100%) |
| accuracy | exact match | Category correctness vs. labeled data |
| <rubric> | LLM-as-judge (different model than the one under test) | Tone/faithfulness/etc. |

## Thresholds (gate conditions)

| Metric | Ship floor (G4 fails below) | Target | Current |
| --- | --- | --- | --- |
| schema_valid | 99% | 100% | |
| accuracy | | | |
| injection resistance | 100% on adversarial set | 100% | |

## Regression policy

- Every prompt or model change ⇒ full eval run; scores in the commit/PR.
- Any metric below ship floor ⇒ failed verify. No averaging away a floor breach.
- Online: sample production outputs on a schedule, score, alert on drift.

## Run

```bash
# wire to harness.config.yaml `verify.eval`, e.g.:
npx evalite run   # or: promptfoo eval -c evals/<behavior>/config.yaml
```
