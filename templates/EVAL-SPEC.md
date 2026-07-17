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
| Model risk governance | <institutional model-inventory registration id / model-risk sign-off reference — required for T1; "not yet registered" is a G2 blocker, not a footnote> |

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

## Model & prompt upgrade protocol

Offline evals green is necessary, not sufficient. A model or prompt swap on a live
feature follows all of this, in order:

1. **Pin the candidate** by exact id; enter the workflow as a change (fast path).
2. **Offline side-by-side**: full suite, incumbent vs candidate, per-category
   floors non-negotiable — injection resistance is re-proven, never grandfathered.
   Below floor ⇒ remediation (prompt re-tune = new version = full re-run) or reject.
3. **Shadow on live traffic** before any cutover: candidate runs in parallel,
   decisions unused; measure **agreement rate** with the incumbent and investigate
   disagreement clusters. Minimum window sized to cover a representative traffic mix.
4. **Pre-decide the deadline rule** where an external cutoff exists (deprecation,
   contract end): if the candidate is not green by the cutoff, the feature
   **degrades to its designed fallback — a below-floor model is never shipped to
   make a date.** Write the rule in the CHANGE before evals start, while nobody is
   tempted.
5. **Cost & latency delta** recorded; denial-of-wallet budgets and alerts
   re-baselined to the candidate's economics.
6. **Human-in-the-loop comms**: people who approve/override the model's output are
   told what's changing and when; watch the override rate through cutover — a
   silent behavior shift shows up there first.
7. **Model inventory / model-risk registration** updated for the material change.
8. **Staged cutover + observation window**: online sampling re-baselined; G5 review
   covers the pin and any prompt version like any other change.

## Run

```bash
# wire to harness.config.yaml `verify.eval`, e.g.:
npx evalite run   # or: promptfoo eval -c evals/<behavior>/config.yaml
```
