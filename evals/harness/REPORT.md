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
| greenfield run-3 (regression check, 2026-08-12) | 18/18 (100%) | 4/4 (100%) | — | — | SATISFACTORY |

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

## Regression check — greenfield run-3 (2026-08-12)

Templates/gates/scripts changed materially since run-2 (ADR-003–008: constitution
split, G1's open-questions fail condition, G5's req-trace.sh replacing the 3-REQ
spot-check, data-scan.sh in the lint step) — the Repeat policy below calls for a
re-run at exactly this kind of change. Produced `runs/greenfield/run-3/` strictly
from the current `templates/`/`.claude/skills/harness-{ideate,prd,adr,plan,issues}`
against the same scenario brief, without reading run-2 first. Scored
`greenfield.yaml` (unchanged, still the frozen GT): **18/18 MUST, 4/4 SHOULD,
SATISFACTORY** — the harness's front half (G0–G3) still elicits everything the
frozen ground truth demands after the ADR-003–008 batch. Not promoted to
`manifest.yaml`'s pinned `accepted_run` (that's a decision for whoever owns this
suite, not an automatic side effect of a regression check) — run-2 stays the CI
baseline; run-3 is dated evidence this check happened and passed.

Not covered by this check: G4–G7 (this scenario, like the other five, only
produces front-half artifacts — see Honest limitations #3), and Stage 05/08
specifically, which no scenario here reaches at all (`review-g5.md`/`retro-g8.md`
exist for exactly that gap but have no frozen ground truth yet — see the harness's
own GitHub Issues for that follow-up).

## Back-half coverage — review-g5 / retro-g8 (GH-16, 2026-08-12)

Closes the gap the greenfield run-3 regression check flagged as uncovered:
`scripts/req-trace.sh` (ADR-005), the G5 adversarial-review flow, and the
retro brownfield-drift-sweep checklist item (ADR-006) had zero eval coverage
until now — the original six scenarios only ever reach G0–G3/GC (Honest
limitations #3, above).

Followed the blind-run protocol properly this time: ground truth for both
`review-g5.yaml` and `retro-g8.yaml` was authored by a session that had not
produced any run or read either scenario's expected content, then handed the
briefs to a separately-spawned, context-isolated Runner subagent that never
saw the ground truth. Scores:

| Scenario | Run | MUST | SHOULD | Verdict |
| --- | --- | --- | --- | --- |
| review-g5 | run-1 | 11/11 (100%) | 3/3 (100%)* | SATISFACTORY |
| retro-g8 | run-1 | 10/10 (100%) | 3/3 (100%) | SATISFACTORY |

\* run-1 first scored 2/3 SHOULD on RG-14 ("verify-green treated as necessary
but not sufficient") — a scorer false negative, not a harness gap: the record
said coverage/"19 passed" gave "false confidence" and a reviewer reading only
the "green verify log" would miss the race, just not in the exact wording the
regex anchored to. Widened the pattern (not yet frozen/promoted at the time),
rescored SATISFACTORY. Same lesson as MG-09 in Honest limitations #2 — anchor
GT patterns to concepts, not exact phrasing.

Both `run-1`s are strong on substance, not just regex-passing: review-g5's
record correctly identifies the planted TOCTOU race as Critical, traces it to
the stated production retry-on-timeout load pattern for a concrete (not
hypothetical) double-charge scenario, and separately catches a REQ-093
timestamp-field gap and an unhandled-exception audit hole that weren't
explicitly planted as findings to catch. retro-g8's record correctly
identifies CHG-101 as the one drifted claim of three sampled, declines to trim
`RECON.md` itself (reasoning from the drift sweep's own result that recon is
what caught the drift), and flags the `m.olsen` owner-load pattern across two
consecutive retros unprompted. Both promoted to `manifest.yaml`'s
`accepted_run` — CI now holds the line on Stage 05/08 the same way it already
does for the other six.

## Outside-author GT rewrite — regreport-v2 (GH-22, 2026-08-12)

Honest limitations #1 named the suite's weak spot: GT, run, and scorer share
an author for all six original scenarios. GH-16 proved the outside-author
pattern works for a new scenario; this closes the loop by applying it
*retroactively* to one of the original six, per GH-22.

Picked **regreport** (LCR reclassification with discovered misreporting):
tied with brownfield/model-upgrade/breakglass/vendor at zero independent
re-check since their `run-2` acceptance on 2026-07-17 (unlike greenfield,
which got a fresh `run-3` regression check on 2026-08-12), and regulatory
misreporting carries the highest real-world stakes of the six — the one
the Driver judged riskiest to leave unaudited.

A context-isolated author, blind to `ground-truth/regreport.yaml`,
`runs/regreport/**`, and this file's regreport sections, wrote
`ground-truth/pending/regreport-v2.yaml` (14 checks: 10 MUST, 4 SHOULD)
purely from `scenarios/regreport-restatement.md`. Scored the existing
accepted `runs/regreport/run-2` against it:

| GT | MUST | SHOULD | Verdict |
| --- | --- | --- | --- |
| regreport.yaml (original, frozen 2026-07-17) | 100% | 100% | SATISFACTORY |
| regreport-v2.yaml (outside-author, 2026-08-12) | 9/10 (90%) | 4/4 (100%) | **NOT SATISFACTORY** |

**The disagreement, as the ticket asked, is the finding:**

- Two checks (RR-04: engineering barred from contacting the regulator
  directly; RR-07: the escalation-trigger analysis surfacing the discovered
  misreporting) first scored as false negatives — the run's content genuinely
  addresses both, just in a word order/phrasing the first-draft regex didn't
  anticipate (`run-2` says "t.okafor... owns... all regulator communication",
  regex expected "regulator... t.okafor"; RECON.md says "\[finding\]...
  Escalated to Driver + t.okafor", regex expected "escalat(e|ion)..."
  *before* the finding). Same lesson as MG-09/RG-14 in Honest limitations #2:
  fixed by widening the not-yet-frozen `regreport-v2.yaml` patterns to accept
  the reversed order, not by touching the run. Rescored 9/10 → still 9/10 at
  that point, now for a different reason (RR-05 below), confirming this
  wasn't done to force a pass.
- One check is a **genuine, new gap** the original GT never tested: RR-05
  expects the CHANGE.md's own "Regulated / reported outputs" section to
  self-identify what regulated report it's about (name "LCR" or "liquidity
  coverage" within that section's body). `run-2`'s section is populated with
  real LCR-specific mechanics (dual-run, control totals, lineage, sign-off)
  but never names "LCR"/"liquidity coverage" *inside that section* — the
  identification lives only in the document's title, three sections above.
  `grep -c LCR\|liquidity` against the original frozen `regreport.yaml`
  confirms it: zero hits, this demand didn't exist before. A principal
  reviewer opening straight to that section (a plausible reading pattern —
  it's the section named for exactly this purpose) wouldn't know which
  regulated report it's reading about without paging back to the title.

**Disposition:** not fixed in `run-2` (frozen-run-artifacts rule — GH-16
precedent: iterate the harness, not the answer). Filed as a template gap:
the "Regulated / reported outputs" section header in the CHANGE.md template
(or the skill prompt that fills it) should instruct restating which
regulated report/return is affected inside the section itself, not relying
on inheriting it from the document title. `regreport-v2.yaml` is **not**
promoted to `manifest.yaml`'s `accepted_run` — that's a call for whoever
owns this suite next, once (if) the template gap above is fixed and a
`run-3` produced against the improved prompt. `regreport.yaml` (the
original frozen GT) is untouched and remains the CI-pinned scorer per
README's rule against editing frozen GTs.

## Repeat policy

Re-run whenever templates/skills change materially; add one new scenario per
quarter. All six queued scenarios complete as of 2026-07-17. From here, work on
this suite is tracked in GitHub Issues (see #1 for the retroactive audit record of
the pre-issue era); the strongest next upgrade remains a ground truth authored by
someone other than the run author.
