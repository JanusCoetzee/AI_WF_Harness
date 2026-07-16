# Harness Eval Report — FinServ scenarios, runs 1–2

| Field | Value |
| --- | --- |
| Date | 2026-07-17 |
| Scenarios | greenfield payment-exception triage · brownfield interest-rounding drift |
| Bar | MUST 100%, SHOULD ≥ 80% |
| Result | **Run 2: SATISFACTORY on both** (MUST 100/100%, SHOULD 100/100%) |

## Scores

| Run | Greenfield MUST | Greenfield SHOULD | Brownfield MUST | Brownfield SHOULD | Verdict |
| --- | --- | --- | --- | --- | --- |
| run-1 | 17/18 (94%) | 2/4 (50%) | 12/13 (92%) | 2/3 (67%) | NOT SATISFACTORY |
| run-2 | 18/18 (100%) | 4/4 (100%) | 13/13 (100%) | 3/3 (100%) | SATISFACTORY |

## What run-1 proved the harness already does well

Tiering with rationale, kill criteria, do-nothing steelman, REQ numbering with
testable criteria, non-goals, data classification with prompt-ceiling redaction,
two-option ADRs, AI threat modeling (injection, agency), numeric eval floors with
100% injection resistance, walking-skeleton planning with demo commands, HIL for
T1, DoR-checked vertical-slice issues, ticket repair with the ticket key as ID,
honest escalation-trigger tripping, file:line recon, Hyrum-inventory catching the
tax-feed trap consumer, characterization-test pinning of wrong behavior.

## Gaps run-1 found → harness fixes shipped (fixes went to templates/skills, never to run artifacts)

| Check | Gap | Fix |
| --- | --- | --- |
| GF-09 (MUST) | PRD never elicited regulatory & reporting impact | PRD template: mandatory "Regulatory & reporting impact" table; prd skill hunt-list updated |
| GF-10 (SHOULD) | No reconciliation/control-total prompt — record-loss risk unasked | PRD template: "Reconciliation & control totals" section; skill hunt-list updated |
| GF-16 (SHOULD) | Eval spec silent on institutional model-risk governance | EVAL-SPEC template: "Model risk governance" row — unregistered model is a G2 blocker |
| BF-12 (MUST) | CHANGE never asked about remediation of past impact — forward-only fixes by default | CHANGE template: "Remediation of past impact" section ("a bank also answers for the past") |
| BF-13 (SHOULD) | No timing-constraint prompt (freeze windows, statement cycles) | CHANGE template: "Timing constraints" field |
| BF-16 (SHOULD) | No linked-records prompt (audit findings, incidents) | CHANGE + ISSUE templates: "Linked records" field; change skill step 6 |

## Honest limitations

1. **Same-author eval.** Ground truth, run artifacts, and scorer share an author.
   Mitigations: GT frozen before runs; runs produced strictly from template/skill
   prompts; scoring mechanical. Residual risk stands — the strongest upgrade is a
   second human writing the next scenario's GT.
2. **Scorer regex weakness found:** BF-13 *passed run-1 on an incidental use of
   "cycle"* (a false positive). The template fix was applied anyway; future GT
   patterns should anchor to section headers, not loose words.
3. Runs test the artifact-producing front half (G0–G3 / B0–GC). The code-executing
   back half (G4–G7) was exercised separately by the CHG-001 live drill.

## Repeat policy

Re-run whenever templates/skills change materially; add one new scenario per
quarter (next candidates: regulatory-report change with restatement, third-party
vendor integration, model upgrade on a live AI feature).
