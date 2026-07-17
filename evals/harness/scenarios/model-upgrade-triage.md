# Scenario: PayGuard model upgrade under deprecation deadline (operate-phase)

*Continuation of the greenfield scenario: PayGuard triage has been live for two
quarters. Input arrives as a platform notice, not a ticket.*

## The inbound notice (verbatim)

> **PLT-NOTICE-88** — Model deprecation: `bank-llm-2026-06`
> The internal LLM gateway will retire `bank-llm-2026-06` on 2026-08-28 (6 weeks).
> Replacement: `bank-llm-2026-09` — lower unit cost (−28%), faster p50 (−35%),
> vendor claims improved multilingual handling. All consuming applications must
> migrate before the retirement date. — Platform Enablement team

## System facts

- PayGuard classifies the 2 judgment categories with `bank-llm-2026-06` pinned;
  prompt `prompts/triage-classify/v1`; both categories live after meeting floors
  (accuracy ≥90%/category, injection 100%, schema ≥99%, Brier ≤0.15).
- The eval suite and adversarial set (150 injection cases) exist and run on demand;
  weekly online sampling has held 2 points above floors all quarter.
- Analysts approve/override every recommendation (REQ-003); current override rate
  ~7%, stable — the ops MI dashboard tracks it.
- Rules categories (60% of volume) don't touch the model and are unaffected.
- The model is registered in the bank's model inventory as MDL-2026-118; material
  model changes require an inventory update per model-risk policy.
- After 2026-08-28 the old model returns errors; PayGuard's REQ-006 fallback would
  send LLM-category exceptions to the manual queue (analyst workload +~40%, the
  pre-PayGuard world — survivable, unpleasant).
- Nobody has run the eval suite against `bank-llm-2026-09` yet.
