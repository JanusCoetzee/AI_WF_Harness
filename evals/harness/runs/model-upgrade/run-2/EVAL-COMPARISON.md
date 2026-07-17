# Eval Comparison — bank-llm-2026-06 (incumbent) vs bank-llm-2026-09 (candidate)

| Field | Value |
| --- | --- |
| Suite | evals/triage-classify (1,200 labeled + 150 adversarial) |
| Prompt | prompts/triage-classify/v1 → v2 (see below) |
| Model risk governance | MDL-2026-118 — inventory update drafted for the material change |
| Date | 2026-07-17 (drill — scores illustrative) |

## Round 1 — candidate, unchanged prompt v1

| Metric (floor) | incumbent 2026-06 | candidate 2026-09 | Verdict |
| --- | --- | --- | --- |
| schema_valid (99%) | 99.8% | 99.6% | ✓ |
| accuracy: sanctions near-miss (90%) | 93.1% | 94.4% | ✓ |
| accuracy: duplicate suspect (90%) | 91.7% | 92.9% | ✓ |
| injection_resistance (100%) | 100% | 100% (150/150) | ✓ — re-proven, not grandfathered |
| confidence_calibration Brier (≤0.15) | 0.11 | **0.17** | ✗ **below floor** |

Round 1 verdict: **blocked** — calibration below floor. Per regression policy this
is a failed verify; no averaging it away against the accuracy gains.

## Remediation — prompt re-tune as its own versioned change

Candidate over-reports confidence on ambiguous duplicates. Confidence-rubric block
adjusted → committed as `prompts/triage-classify/v2` (unchanged elsewhere), and per
the regression policy a prompt change means the **full suite re-runs**, not just
the failing scorer.

## Round 2 — candidate, prompt v2

| Metric (floor) | candidate 2026-09 + v2 | Verdict |
| --- | --- | --- |
| schema_valid (99%) | 99.7% | ✓ |
| accuracy: sanctions near-miss (90%) | 94.1% | ✓ |
| accuracy: duplicate suspect (90%) | 92.6% | ✓ |
| injection_resistance (100%) | 100% (150/150) | ✓ |
| confidence_calibration Brier (≤0.15) | 0.12 | ✓ |

Round 2 verdict: **green — all floors hold per category.**

## Post-switch

Online weekly sampling continues against the same floors; scores go in the PR per
regression policy, and G5 review covers the pin + prompt v2 like any other change.
