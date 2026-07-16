# PLAN — PayGuard exception triage

| Field | Value |
| --- | --- |
| Status | Ratified (G3) — drill |
| Re-planning checkpoint | end of M2 (plan spans ~9 weeks) |
| PRD | ./PRD.md |

## Milestone map

Sequenced riskiest-assumption-first: classification quality and redaction
feasibility are the bets that kill this project; they get proven before any UI work.

| # | Milestone (behavior) | Demo command | Proves / kills which risk |
| --- | --- | --- | --- |
| M0 | Walking skeleton: one synthetic hub event flows topic → triage-svc → redaction stub → gateway echo → recommendation store → visible in case tool sandbox; CI + deploy to dev | `make demo-m0` (publishes event, tails recommendation) | Integration risk across all five systems |
| M1 | Rules classify the 4 deterministic categories from status codes; routing matrix as config | `make demo-m1 CASE=format-fail` | 60% of volume needs no model at all |
| M2 | LLM classifies the 2 judgment categories **in shadow**; eval suite green at floors incl. injection 100%; redaction meets DPO standard | `make demo-m2` (runs eval suite, prints scores) | THE risk: classification quality + redaction feasibility (kill criteria live here) |
| M3 | Analyst approve/override UI slice; audit trail reconstructs a decision end-to-end | `make demo-m3 CASE=sanctions-hold` | HIL workflow actually fits analyst practice |
| M4 | Per-category live enablement behind flags; sanctions category last, with compliance sign-off | `make demo-m4` (flips one category, shows live routing + audit) | Progressive rollout machinery |

## Milestone detail (M0 shown; M1–M4 follow the same shape)

### M0 — Walking skeleton

- Tasks (each ≤ half a day, REQ-mapped):
  - [ ] T0.1 scaffold triage-svc + CI + dev deploy (REQ-102)
  - [ ] T0.2 consume hub topic, schema-validate events (REQ-001)
  - [ ] T0.3 redaction-service stub behind interface (data inventory)
  - [ ] T0.4 gateway echo call with pinned model id (REQ-201)
  - [ ] T0.5 recommendation store + case tool sandbox render (REQ-002)
- Test strategy: contract tests on event schema; integration test on the full slice.
- Demo command: `make demo-m0`
- Demo record: (at completion)

## Out-of-plan proposals

| Date | Proposal | Disposition |
| --- | --- | --- |

## Plan change log

| Date | Change | Reason | Approved by |
| --- | --- | --- | --- |
