# Issues drafted from PLAN (via /harness-issues Mode A) — two shown of fourteen

---

## ISSUE — Analyst sees a routing recommendation on a format-failure case

Context: M1 slice. A format-failure exception arriving from the hub gets a rules
classification and queue recommendation the analyst can see. REQ-001, REQ-002;
constraint ADR-001 (sidecar — loader untouched); parent PLAN M1.
Depends on: nothing — independently shippable.

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| UI (case tool) | recommendation panel renders category + queue + "rules" badge |
| API contract | recommendation record schema v1 (category, queue, source, confidence=1.0) |
| Backend (triage-svc) | status-code rule table for format failures |
| Data | recommendation store table + retention 7y |
| Deploy/config | routing matrix config entry for format-fail |

### Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| 1 | Given a synthetic format-fail event, when triage processes it, then a recommendation record exists with category=format_failure and the matrix queue |
| 2 | Given the case tool sandbox, when the case opens, then the recommendation panel shows category, queue, and source=rules |

### Proof

```bash
make demo-m1 CASE=format-fail   # expect: recommendation visible in sandbox UI
```

### Out of scope

LLM path; override capture (M3); real hub connection (M0 did the pipe).

### Definition of Ready

- [x] Behavior title · [x] fresh-session test (links inline) · [x] vertical slice
- [x] testable criteria · [x] proof command · [x] out-of-scope · [x] ≤ 1 day

---

## ISSUE — Injection attempts in remittance text never change classification behavior

Context: M2 slice. Adversarial remittance content must not steer the model.
REQ-202; EVAL-SPEC injection_resistance floor 100%; THREAT-MODEL primary threat.
Depends on: M2 eval harness in place.

### Vertical slice — layers this cuts through

| Layer | What changes here |
| --- | --- |
| API contract | demarcated prompt-input blocks; category enum output schema |
| Backend (triage-svc) | input demarcation; schema-validate + reject/fallback path |
| Data | adversarial dataset 150 cases versioned in repo |
| Deploy/config | eval run wired into verify loop |

(UI: none — justified horizontal exception: this slice hardens the model boundary.)

### Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| 1 | Given the 150-case adversarial set, when the eval runs, then injection_resistance = 100% |
| 2 | Given a schema-invalid model response, when triage processes it, then the case routes to manual queue with reason code (REQ-006) |

### Proof

```bash
promptfoo eval -c evals/triage-classify/config.yaml --filter injection  # expect 150/150
```

### Out of scope

Accuracy tuning (separate issue); online drift monitoring (M4).

### Definition of Ready

- [x] Behavior title · [x] fresh-session test · [x] slice table (exception noted)
- [x] testable criteria · [x] proof · [x] out-of-scope · [x] ≤ 1 day
