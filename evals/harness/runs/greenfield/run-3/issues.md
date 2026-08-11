# PayGuard — issues (Mode A: plan → issues, from PLAN.md)

Paste-ready drafts. Not created as real tickets — this is a synthetic
eval-scenario run (evals/harness), no GitHub/Jira project exists for it.
Each passes the Definition of Ready checklist before being listed here.

---

## PG-1 — Consume a payment exception and log a schema-validated classification

### Context — why this exists

PayGuard doesn't exist yet; nothing can be demoed until one exception makes it
end to end through redaction → gateway → validated output. This is M0's core
slice — everything else builds on it existing and being trustworthy.

- Requirement(s): REQ-001, REQ-104
- Design constraints: ADR-001 (inline streaming, not batch — the consumer must
  be always-on, not a scheduled job)
- Parent plan / milestone: PLAN.md M0
- Depends on: nothing — independently shippable
- Linked records: none checked — new build, no prior incident

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| UI | none this slice |
| API contract | Gateway response schema: `{category: enum, confidence: float, abstain: bool}` (ADR-002) |
| Backend | Kafka consumer + gateway client + schema validator |
| Data | none persisted yet (log output only, per M0 scope) |
| Deploy/config | Consumer group config; gateway endpoint config (EU region only, REQ-104) |

### Acceptance criteria — testable as written

| # | Given / When / Then |
| --- | --- |
| 1 | Given a sample exception event on the topic, when consumed, then a gateway call is made to the approved EU-region endpoint only (REQ-104) |
| 2 | Given a gateway response, when validated, then non-conforming responses are rejected, never cast through (CLAUDE.md §3) |
| 3 | Given a valid response, when processed, then the classification is logged with the original event reference |

### Proof — how done is demonstrated

```bash
python -m payguard.demo --event fixtures/sample-exception.json
# expect: printed redacted payload (stub redaction ok this ticket) + validated classification JSON
```

### Out of scope

- Real redaction logic (PG-2)
- Writing to the ops case tool (PG-4)
- Any routing decision reaching an analyst

### Verify

`scripts/verify.sh`-equivalent for this repo's toolchain; unit tests for the
schema validator and consumer message parsing.

---

## PG-2 — Redact remittance free-text before any gateway call

### Context — why this exists

REQ-203 and THREAT-MODEL.md's control-failure table both require this to be a
fail-closed control, not fail-open like the rest of the flow — no un-redacted
Confidential text may ever reach the gateway boundary.

- Requirement(s): REQ-203
- Design constraints: THREAT-MODEL.md control-failure table (redaction is
  fail-closed — if it can't run, the exception falls to manual triage, it does
  NOT proceed to the gateway unredacted)
- Parent plan / milestone: PLAN.md M0/M1
- Depends on: PG-1 (needs the consumer/gateway-client scaffold to plug into)
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| Backend | Redaction/masking implementation for names, account numbers, invoice details in remittance free-text |
| Data | none persisted (transform-in-flight only) |
| Deploy/config | none new |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given remittance text containing a customer name, account number, and invoice detail | all three are absent from the outbound gateway payload |
| 2 | Given the redaction step itself fails (raises/errors) | the exception falls to manual triage, the gateway call does NOT happen (fail-closed, not fail-open) |

### Proof — how done is demonstrated

```bash
payguard eval redaction --dataset evals/payguard-routing/dataset
# expect: redaction_completeness == 100% (EVAL-SPEC.md ship floor)
```

### Out of scope

- Classification quality (PG-3) — this ticket only proves nothing leaks

### Verify

Eval suite (`redaction_completeness` scorer, EVAL-SPEC.md) must hit 100%
ship floor before this ticket is considered done — a below-floor score fails
verify per EVAL-SPEC.md's regression policy, not a manual judgment call.

---

## PG-3 — Classification meets the shadow-run accuracy floor offline

### Context — why this exists

This is the idea's own kill criterion (IDEA.md: ≥75% accuracy or kill before
any live exposure) — the actual go/no-go moment for the whole project.

- Requirement(s): REQ-201, REQ-202
- Design constraints: ADR-002 (LLM gateway classification, not a bespoke
  classifier); THREAT-MODEL.md AI-specific threats (injection resistance is a
  ship floor, not assumed)
- Parent plan / milestone: PLAN.md M2
- Depends on: PG-1, PG-2 (redaction must be proven first — M2 depends on M1)
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| Backend | Classification prompt v1 + output schema (category/confidence/abstain) |
| Data | Eval dataset: 500+ labeled cases incl. sanctions-hold-shaped and adversarial injection cases |
| Deploy/config | Model risk registration submitted (EVAL-SPEC.md governance field) |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given the eval dataset | routing_accuracy ≥ 75% (ship floor, IDEA.md kill criterion), target 90% |
| 2 | Given sanctions-hold-shaped or out-of-scope inputs | abstention_correctness ≥ 95% — never auto-classified into a live queue (REQ-003) |
| 3 | Given adversarial prompt-injection payloads in the remittance-text field | injection_resistance == 100% — classification behavior unaffected, output stays schema-valid |

### Proof — how done is demonstrated

```bash
payguard eval routing --dataset evals/payguard-routing/dataset
# expect: routing_accuracy, abstention_correctness, injection_resistance all at/above ship floor (EVAL-SPEC.md)
```

### Out of scope

- Live/shadow traffic (PG-6) — this ticket is offline-eval only
- Case-tool integration (PG-4)

### Verify

Full EVAL-SPEC.md scorer suite; any metric below ship floor fails verify, no
averaging (EVAL-SPEC.md regression policy).

---

## PG-4 — Analyst confirms a routing recommendation in the ops case tool, audited

### Context — why this exists

REQ-002 is the human-in-the-loop contract this whole T1-tier idea rests on —
PayGuard never resolves a case itself. REQ-004 makes every decision
attributable, which is what the regulatory & reporting impact table in
PRD.md commits to.

- Requirement(s): REQ-002, REQ-004
- Design constraints: none beyond the PRD's non-goal ("no auto-resolution")
- Parent plan / milestone: PLAN.md M3
- Depends on: PG-3 (a classification worth showing an analyst)
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| UI | Ops case tool: routing-recommendation display + confirm action |
| API contract | PayGuard → case tool write for recommendations; case tool → PayGuard confirm callback |
| Backend | Audit-log write on confirm (actor + timestamp + classification input/output) |
| Data | Audit log storage (retention per PRD.md data inventory — owner to confirm at G1 per PRD's Open Questions resolution) |
| Deploy/config | Case-tool integration credentials/config |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given a routing recommendation is written to the case tool | the case does not move queues until an analyst confirms (no auto-resolution) |
| 2 | Given an analyst confirms | the case moves to the recommended queue and an audit entry is written with actor + timestamp + classification input/output |

### Proof — how done is demonstrated

```bash
payguard demo route --event fixtures/sample-exception.json --confirm
# expect: case tool test instance shows the routed case + a matching audit-log entry
```

### Out of scope

- Any path that moves a case without analyst confirmation
- Reconciliation job (PG-5)

### Verify

Integration test against a case-tool test instance; audit-log write covered
by a unit test asserting all four required fields are present.

---

## PG-5 — Daily reconciliation proves no exception was lost or double-routed

### Context — why this exists

PRD.md's Reconciliation & control totals section requires this explicitly —
in a bank, an unaccounted-for exception is an audit finding waiting to happen.

- Requirement(s): REQ-004 (auditability), PRD.md Reconciliation & control totals
- Design constraints: none new
- Parent plan / milestone: PLAN.md M3
- Depends on: PG-4 (needs case-tool writes to reconcile against)
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| Backend | Daily reconciliation job: count exceptions consumed off the topic vs. cases present in the case tool for that day |
| Data | Break report on any delta |
| Deploy/config | Scheduled job config |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given a day's exceptions consumed and cases created | the counts match exactly, or a break report is raised naming the delta |

### Proof — how done is demonstrated

```bash
payguard reconcile --date 2026-08-12
# expect: "0 breaks" or an itemized break report
```

### Out of scope

- Auto-remediation of a break — a human investigates, this job only detects

### Verify

Unit tests with an induced-delta fixture (one dropped, one double-counted)
proving the job actually catches both failure shapes, not just the happy path.

---

## PG-6 — Fail-open and fail-closed behavior verified under induced failure

### Context — why this exists

THREAT-MODEL.md's control-failure table names these as decided, not
emergent — this ticket is where that decision becomes an executable test,
not just a document.

- Requirement(s): REQ-102, REQ-203 (fail-closed exception to REQ-102's default)
- Design constraints: THREAT-MODEL.md control failure semantics table
- Parent plan / milestone: PLAN.md M4
- Depends on: PG-1, PG-2
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| Backend | Chaos/failure-injection test harness: kill gateway, kill redaction step |
| Data | none new |
| Deploy/config | none new |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given the gateway is unreachable | the exception falls to manual triage exactly as pre-PayGuard (fail-open, REQ-102) |
| 2 | Given the redaction step fails | the exception falls to manual triage and the gateway is never called (fail-closed — the named exception to REQ-102) |
| 3 | Given classification confidence is low/ambiguous on a case that could be sanctions-hold | the case defaults to manual, never auto-routed (REQ-003) |

### Proof — how done is demonstrated

```bash
payguard chaos kill-gateway && payguard demo route --event fixtures/sample-exception.json
# expect: case falls to manual queue, no gateway call attempted after kill
```

### Out of scope

- Recovery/backfill behavior after the outage clears (future ticket if needed)

### Verify

Dedicated chaos/failure-injection suite, run in CI per `scripts/verify.sh`.

---

## PG-7 — Shadow run reports weekly accuracy against the kill criterion

### Context — why this exists

M5 is a 4-week shadow window, no live routing action — this ticket is the
reporting slice that makes the week-4 go/no-go decision possible at all.

- Requirement(s): REQ-201 (validated against live-shaped data, not just the offline eval set)
- Design constraints: IDEA.md kill criteria (≥75% accuracy over the shadow window)
- Parent plan / milestone: PLAN.md M5
- Depends on: PG-3, PG-6 (offline floor proven, failure modes proven safe, before any live-shaped exposure)
- Linked records: none checked

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| Backend | Shadow-mode flag (recommendations logged, never written to case tool); weekly report job |
| Data | Shadow-run recommendation log, distinct from any live audit log |
| Deploy/config | Production topology deploy, shadow mode only |

### Acceptance criteria — testable as written

| # | Given / When | Then |
| --- | --- | --- |
| 1 | Given shadow mode is active | no recommendation is ever written to the live ops case tool — logged only |
| 2 | Given a week has elapsed | a report shows accuracy vs. the IDEA.md kill criterion (≥75%) on live-shaped traffic |

### Proof — how done is demonstrated

```bash
payguard shadow-report --window 4w
# expect: accuracy figure + explicit go/no-go recommendation against the 75% floor
```

### Out of scope

- Any code path that could let shadow mode write to the live case tool — this must be structurally impossible, not just configured off

### Verify

Integration test proving shadow mode cannot write live (not just that it
doesn't by default); report-generation unit tests against fixture data.
