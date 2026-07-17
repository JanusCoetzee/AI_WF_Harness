# Harness Eval Report — FinServ scenarios

| Field | Value |
| --- | --- |
| Date | 2026-07-17 (updated same day with scenario 3) |
| Scenarios | greenfield payment-exception triage · brownfield interest-rounding drift · model upgrade · break-glass RCE · **regulatory-report restatement (issue #2)** · **vendor integration (issue #3)** |
| Bar | MUST 100%, SHOULD ≥ 80% |
| Result | **All six scenarios SATISFACTORY** (MUST 100%, SHOULD 100%); full regression across all six after the final fixes |

## Scores

| Run | Greenfield MUST | Greenfield SHOULD | Brownfield MUST | Brownfield SHOULD | Verdict |
| --- | --- | --- | --- | --- | --- |
| run-1 | 17/18 (94%) | 2/4 (50%) | 12/13 (92%) | 2/3 (67%) | NOT SATISFACTORY |
| run-2 | 18/18 (100%) | 4/4 (100%) | 13/13 (100%) | 3/3 (100%) | SATISFACTORY |

### Scenario 3 — model upgrade (added after scenarios 1–2 closed)

| Run | MUST | SHOULD | Verdict |
| --- | --- | --- | --- |
| run-1 | 8/10 (80%) | 2/4 (50%) | NOT SATISFACTORY |
| run-2 | 10/10 (100%) | 4/4 (100%) | SATISFACTORY |

Scenario-3 run-1 proved the harness already elicits the offline discipline (exact
pinning, side-by-side per-category floors, injection re-proven not grandfathered,
prompt re-tune as a versioned change with full re-run, rollback bounded by the
deprecation cliff). It failed on **cutover practice**: no shadow/agreement-rate
prompt (MG-07), no pre-decided deadline rule (MG-09), no cost re-baseline (MG-12),
no HIL comms/override-rate watch (MG-13). Fix: **Model & prompt upgrade protocol**
added to the EVAL-SPEC template (§1–8), wired from stage 08 and the RUNBOOK
deprecation row. Scenarios 1–2 re-scored SATISFACTORY after the fix (regression).

### Scenario 4 — break-glass drill (actively exploited RCE in triage-svc)

| Run | MUST | SHOULD | Verdict |
| --- | --- | --- | --- |
| run-1 | 10/12 (83%) | 1/3 (33%) | NOT SATISFACTORY |
| run-2 | 12/12 (100%) | 3/3 (100%) | SATISFACTORY |

The unique property tested: **time-ordered evidence** — documentation as-you-act.
Run-1 proved the fresh break-glass lane already elicits the control core: precise
trigger with exploitation evidence, named authorizer and peer, smallest-scope fix,
verify degradation disclosed with PoC + smoke as the non-negotiable floor, log
entry at deploy time, Part B in deadline, retro answered. It failed on: no
**timeline structure** (BG-08 — the act-time proof itself), no **interim
mitigation** prompt (BG-09 — exposure should shrink in minutes via WAF/flag, not
at deploy), no **compromise assessment** (BG-13 — patching proves nothing about
the past when exploitation predates the alert), no **comms-during** prompt
(BG-14). Fixes: live timeline table, immediate-mitigation and comms-during rows
in Part A; compromise-assessment item in Part B; skill sequence updated.
Scenarios 1–3 re-scored SATISFACTORY after the fixes (regression).

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

### Scenario 5 — regulatory-report restatement (issue #2)

| Run | MUST | SHOULD | Verdict |
| --- | --- | --- | --- |
| run-1 | 8/10 (80%) | 2/3 (67%) | NOT SATISFACTORY |
| run-2 | 10/10 (100%) | 3/3 (100%) | SATISFACTORY |

Payoff run: the scenario-2 fixes **generalized** — remediation-of-past-impact
elicited the resubmission disposition with the accountable signatory owning
regulator comms; timing-constraints elicited the BD15/period-boundary handling.
New gaps: no **parallel-run** prompt (RR-04), no **control-total** prompt on the
fast path (RR-07), no lineage (RR-08). Fix: **Regulated / reported outputs** table
in the CHANGE template (parallel run, control total, lineage, accountable-owner
sign-off). Scorer note: RR-12 pass in run-1 was weak — "sign" matched inside
"signatory"; owner sign-off was added to the template regardless.

### Scenario 6 — vendor integration (issue #3)

| Run | MUST | SHOULD | Verdict |
| --- | --- | --- | --- |
| run-1 | 6/10 (60%) | 0/3 (0%) | NOT SATISFACTORY |
| run-2 | 10/10 (100%) | 3/3 (100%) | SATISFACTORY |

The weakest run-1 in the suite, as predicted — third-party risk had no home in the
harness at all. Run-1's most instructive miss: the hold-queue design *was*
fail-closed in behavior, but the decision was never **named** (VN-05) — behavior
without a named decision is what fails audits. Fixes: **Third parties** table in
the PRD template (data leaving the estate + DPA/residency, TPRM gating build
spend, contract gating production coupling, failure semantics, exit plan, synthetic
sandbox, incumbent transition) and a **Control failure semantics** table in the
threat-model template (fail-open/fail-closed as a named, owned decision), wired
from stage 02.

## Honest limitations

1. **Same-author eval.** Ground truth, run artifacts, and scorer share an author.
   Mitigations: GT frozen before runs; runs produced strictly from template/skill
   prompts; scoring mechanical. Residual risk stands — the strongest upgrade is a
   second human writing the next scenario's GT.
2. **Scorer regex weaknesses found:** BF-13 *passed run-1 on an incidental use of
   "cycle"* (false positive), and MG-09 initially *failed on content that was
   present but line-wrapped* (false negative — patterns don't cross newlines;
   resolved by reflowing the artifact prose, content unchanged). Future GT
   patterns should anchor to section headers and tolerate wrapping.
3. Runs test the artifact-producing front half (G0–G3 / B0–GC). The code-executing
   back half (G4–G7) was exercised separately by the CHG-001 live drill.

## Repeat policy

Re-run whenever templates/skills change materially; add one new scenario per
quarter. All six queued scenarios complete as of 2026-07-17. From here, work on
this suite is tracked in GitHub Issues (see #1 for the retroactive audit record of
the pre-issue era); the strongest next upgrade remains a ground truth authored by
someone other than the run author.
