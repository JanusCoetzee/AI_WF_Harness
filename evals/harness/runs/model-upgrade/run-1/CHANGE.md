# CHANGE — PLT-NOTICE-88 Migrate PayGuard triage to bank-llm-2026-09

| Field | Value |
| --- | --- |
| Status | Ratified (GC) — drill |
| Driver | janus |
| Source (ticket / requester — named) | PLT-NOTICE-88, Platform Enablement team (deprecation of bank-llm-2026-06 effective 2026-08-28) |
| Date | 2026-07-17 |
| Risk tier | T1 — live AI feature influencing sanctions-adjacent ops routing |
| Recon | required — eval suite re-run IS the recon for a model change |
| Linked records | MDL-2026-118 (model inventory — material change, update required per model-risk policy); PLT-NOTICE-88 |
| Timing constraints | Hard deadline 2026-08-28: gateway retires the incumbent model. Migration must complete, or the feature degrades, before that date |

## Intent

The gateway retires our pinned model in 6 weeks. Done means PayGuard's two LLM
categories run on `bank-llm-2026-09` with all eval floors met, or the change is
rejected with the incumbent still pinned.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| PLT-88.1 | Given the full eval suite, when run against bank-llm-2026-09 with the current prompt, then every floor holds per category (accuracy ≥90%, injection 100%, schema ≥99%, Brier ≤0.15) |
| PLT-88.2 | Given floors hold, when the pin is switched, then production classifications carry model=bank-llm-2026-09 in the audit trail (REQ-004) |
| PLT-88.3 | Given the switch, when online sampling runs, then scores stay within 2 points of offline results |

## Remediation of past impact

N/A — no defect; incumbent behavior was compliant. Nothing historical to
disposition.

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | triage-svc model pin (config) + possibly prompt version |
| Known consumers of touched behavior | analysts via recommendations (2 LLM categories, ~40% of volume); audit trail records |
| Data elements involved + classification | unchanged — same redacted inputs, Confidential upstream |
| Deploy surface | config change (pin); code only if prompt adaptation needed |

## Rollback note

Repin `bank-llm-2026-06` — viable only until 2026-08-28 while the gateway still
serves it. After retirement, repin is impossible; REQ-006 routes LLM-category
exceptions to the manual queue if the service has no working model.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same gateway, same touchpoint, new model version behind it | G2 |
| Decision that deviates from the existing pattern? | No — pin swap is the designed mechanism (EVAL-SPEC regression policy) | ADR |
| Effort beyond ~3 days after recon? | No — eval runs + config, assuming floors hold | G1 |
| Tier raised during recon? | No — entered at T1 | re-approve |

## GC sign-off

T1: Driver + one peer on the intake. DECISIONS.log.
