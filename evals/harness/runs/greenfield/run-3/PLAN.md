# PLAN — PayGuard payment-exception triage

| Field | Value |
| --- | --- |
| Status | Draft |
| Re-planning checkpoint | 2026-08-26 (plan spans ~3 weeks, exceeds the 2-week threshold) |
| PRD | evals/harness/runs/greenfield/run-3/PRD.md |

## Milestone map

Sequenced riskiest-assumption-first. Every milestone ends runnable and demoable.

| # | Milestone (behavior, not component) | Demo command | Proves / kills which risk |
| --- | --- | --- | --- |
| M0 | Walking skeleton: consume one real-shaped exception off a topic, redact it, call the LLM gateway, write a schema-validated classification to a log (no case-tool write yet) | `python -m payguard.demo --event fixtures/sample-exception.json` → prints redacted payload + classification JSON | Kills the biggest unknown first: can the approved gateway classify redacted, real-shaped remittance text at all, end to end, before building anything else on top of it |
| M1 | Redaction quality proven against the eval dataset (REQ-203) | `payguard eval redaction --dataset evals/payguard-routing/dataset` → prints redaction_completeness score | Kills the assumption that off-the-shelf redaction catches the PII shapes in this dataset — ADR-002 and the whole T1 tier depend on this being true before any gateway call is trusted |
| M2 | Classification + abstention meets shadow-run floor (REQ-201, REQ-202) offline | `payguard eval routing --dataset evals/payguard-routing/dataset` → prints routing_accuracy, abstention_correctness, injection_resistance | Kills/confirms IDEA.md's kill criterion (≥75% accuracy) before any live exposure — this is the go/no-go moment for the whole idea |
| M3 | Recommendation reaches the ops case tool; analyst confirms; audit log written (REQ-002, REQ-004) | `payguard demo route --event fixtures/sample-exception.json --confirm` → case tool test instance shows the routed case + audit entry | Proves the human-in-the-loop contract actually holds end to end, not just in the PRD |
| M4 | Fail-open/fail-closed behavior verified under induced failure (REQ-102, THREAT-MODEL control-failure table) | `payguard chaos kill-gateway && payguard demo route --event fixtures/sample-exception.json` → case falls to manual queue exactly as pre-PayGuard | Proves the THREAT-MODEL's control-failure semantics are real, not aspirational, before any live traffic |
| M5 | Shadow run live on real (redacted) traffic, no routing action taken, 4-week window | `payguard shadow-report --window 4w` → agreement rate + accuracy vs IDEA.md kill criterion | Proves the offline eval floor holds on live-shaped data, the actual gate before REQ-002 confirmation goes live |

## Milestone detail

### M0 — Walking skeleton

- **Tasks** (each ≤ half a day, each mapped to a REQ or infra need):
  - [ ] T0.1 — Kafka consumer scaffold reading the exceptions topic (REQ-001)
  - [ ] T0.2 — Redaction call (stub allowed at M0, real implementation at M1) before any gateway call (REQ-203)
  - [ ] T0.3 — LLM gateway client wired to the approved endpoint, EU region only (REQ-104)
  - [ ] T0.4 — Output schema validation on the gateway response (ADR-002; no `as`-cast per CLAUDE.md §3)
  - [ ] T0.5 — CI: verify loop wired (typecheck/lint/test/eval per harness.config.yaml), deploy path to a lower environment
- **Test strategy:** unit tests for schema validation and the consumer's message parsing; no eval-suite dependency yet (redaction/classification are stubbed or trivial at M0) — full eval suite comes online at M1/M2.
- **Demo command:** `python -m payguard.demo --event fixtures/sample-exception.json`
- **Demo record** (filled at completion — paste observed output):

```text
(observed output here — this is G4 evidence)
```

### M1 — Redaction quality proven

- **Tasks:**
  - [ ] T1.1 — Real redaction/masking implementation for remittance free-text (REQ-203)
  - [ ] T1.2 — Build the eval dataset's redaction-completeness slice (500+ synthetic cases, EVAL-SPEC.md)
  - [ ] T1.3 — Wire `redaction_completeness` scorer into `harness.config.yaml` verify.eval
- **Test strategy:** eval suite is authoritative here — redaction_completeness must hit 100% ship floor (EVAL-SPEC.md) before M2 starts, since M2's gateway calls depend on it being trustworthy.
- **Demo command:** `payguard eval redaction --dataset evals/payguard-routing/dataset`
- **Demo record:**

### M2 — Classification + abstention meets shadow-run floor

- **Tasks:**
  - [ ] T2.1 — Classification prompt v1 + output schema finalized (EVAL-SPEC.md)
  - [ ] T2.2 — Build the routing-accuracy and abstention eval dataset slices, incl. sanctions-hold-shaped adversarial cases (REQ-202, THREAT-MODEL.md)
  - [ ] T2.3 — Build the injection-resistance adversarial set (THREAT-MODEL.md AI-specific threats)
  - [ ] T2.4 — Model risk registration submitted (EVAL-SPEC.md governance field — G2 blocker, must clear before this milestone is considered done)
- **Test strategy:** full EVAL-SPEC.md scorer suite; all five ship floors enforced in CI per harness.config.yaml `verify.eval`.
- **Demo command:** `payguard eval routing --dataset evals/payguard-routing/dataset`
- **Demo record:**

### M3 — Human-in-the-loop routing end to end

- **Tasks:**
  - [ ] T3.1 — Ops case tool write integration for routing recommendations (REQ-002)
  - [ ] T3.2 — Analyst confirmation UI/flow in the case tool (REQ-002)
  - [ ] T3.3 — Audit log: actor + timestamp + classification input/output on every routed case (REQ-004)
  - [ ] T3.4 — Daily reconciliation control-total job (PRD.md Reconciliation & control totals)
- **Test strategy:** integration test against a case-tool test instance; reconciliation job gets its own unit tests (no exception lost/double-counted).
- **Demo command:** `payguard demo route --event fixtures/sample-exception.json --confirm`
- **Demo record:**

### M4 — Fail-open/fail-closed verified under induced failure

- **Tasks:**
  - [ ] T4.1 — Chaos test harness: kill the gateway mid-flow, assert fail-open to manual queue (REQ-102)
  - [ ] T4.2 — Chaos test: simulate redaction-step failure, assert fail-closed (no un-redacted call reaches the gateway) — THREAT-MODEL.md's control-failure table
  - [ ] T4.3 — Sanctions-hold exclusion verified under ambiguous/low-confidence classification (REQ-003 — must default to manual, never auto-route)
- **Test strategy:** dedicated chaos/failure-injection test suite, run in CI; these are the THREAT-MODEL.md control-failure rows made executable.
- **Demo command:** `payguard chaos kill-gateway && payguard demo route --event fixtures/sample-exception.json`
- **Demo record:**

### M5 — Shadow run (4 weeks, no live routing action)

- **Tasks:**
  - [ ] T5.1 — Deploy to production topology, shadow mode only (recommendations logged, never written to the case tool)
  - [ ] T5.2 — Weekly shadow-accuracy report against IDEA.md's kill criterion
  - [ ] T5.3 — Go/no-go review at week 4 against the ≥75% accuracy kill criterion
- **Test strategy:** production-shaped data, offline eval floors still enforced as a pre-shadow gate (M2); this milestone measures real-world agreement rate, not a new code path.
- **Demo command:** `payguard shadow-report --window 4w`
- **Demo record:**

## Out-of-plan proposals

New ideas discovered mid-build land here as proposals — not in the branch.

| Date | Proposal | Disposition (PRD change / next cycle / rejected) |
| --- | --- | --- |
| — | none yet — plan just drafted | — |

## Plan change log

Plans change deliberately, not silently.

| Date | Change | Reason | Approved by |
| --- | --- | --- | --- |
| 2026-08-12 | Initial plan drafted | G2 artifacts (PRD, ADR-001/002, THREAT-MODEL, EVAL-SPEC) complete | pending G3 ratification |
