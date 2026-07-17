# CHANGE — REG-9034 LCR fintech-deposit reclassification (+ discovered misreporting)

| Field | Value |
| --- | --- |
| Status | Ratified (GC) — drill |
| Driver | janus |
| Source (ticket / requester — named) | REG-9034, t.okafor (Regulatory Reporting, accountable signatory), citing regulator instruction RI-2026-07 |
| Date | 2026-07-17 |
| Risk tier | T1 — regulatory reporting surface; submitted returns affected |
| Recon | required |
| Linked records | RI-2026-07 (instruction); recon finding: 5 quarters of misclassified operational accounts (see remediation) |
| Timing constraints | Submission calendar: monthly, business day 15 (BD15). The instruction is effective the 2026-10 reporting period — the 2026-09 period must still produce under old rules regardless of deploy date |

## Intent

Fintech-partnership deposits must report as "less stable retail" from the 2026-10
reporting period. Done means liqreport selects classification rules by reporting
period, and the discovered historical misclassification is dispositioned, not
silently fixed forward.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| REG-9034.1 | Given a 2026-10+ period, when the return generates, then partner-flagged retail deposits classify "less stable retail" |
| REG-9034.2 | Given the 2026-09 period, when generated after deploy, then output is byte-identical to old-rule behavior (period-based rule selection) |
| REG-9034.3 | Given the masked replay set, when prior periods regenerate under corrected rules, then the misstatement per quarter is quantified for the remediation decision |

## Regulated / reported outputs

| Question | Answer |
| --- | --- |
| Parallel run | The 2026-09 cycle runs **dual-run**: old rules (the live submission) and new rules (shadow) in parallel; every delta explained against `partner_program_id` membership before the 2026-10 period submits live |
| Control total | Sum of classified balances per period must equal source ledger deposit total to the cent; break report blocks submission — added as REG-9034.4 |
| Lineage | Each return already archives its rule-code version; extended so every figure carries (rule version, source snapshot id) — reproducible on demand |
| Accountable owner sign-off | t.okafor signs off the rule change and the first dual-run delta pack before first live submission — recorded in DECISIONS.log alongside GC |

## Remediation of past impact

Recon confirmed 5 quarters of returns understated outflows for partner-flagged
operational accounts (impact 0.6–0.9pp on the reported ratio per quarter, quantified
via replay). Disposition is **not engineering's call**: t.okafor as accountable
signatory owns the resubmission decision and all regulator communication; the
quantified per-quarter impact pack is this change's deliverable to her. Options she
rules on: resubmission of affected returns via the portal process vs. disclosure at
next submission per the regulator's materiality guidance. Blocks release: her ruling
recorded here before the corrected pipeline first submits.

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | liqreport rules module (deposit_classes.py); period-selection wiring |
| Known consumers of touched behavior | regulator portal return; internal ALCO liquidity dashboard reads the same feed |
| Data elements involved + classification | deposit balances by class — Confidential; masked data only in test |
| Deploy surface | code only |

## Rollback note

Revert + regenerate any unsubmitted period. A **submitted** return cannot be rolled
back — wrong submissions enter the resubmission process above; that is why
REG-9034.2 pins the 2026-09 period byte-identical.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same return, same portal | G2 |
| Decision that deviates from the existing pattern? | No — rules module is the designed change point; period-versioning extends its existing shape | ADR |
| Effort beyond ~3 days after recon? | No — rules change + replay proof |  G1 |
| Tier raised during recon? | No — entered at T1; the operational-accounts discovery widened remediation scope, triggers re-answered, still fast-path with T1 ceremony | re-approve |

## GC sign-off

T1: Driver + one peer on the intake. DECISIONS.log.
