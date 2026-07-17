# Harness Evals

The harness applies eval discipline to everything AI-powered — including itself.
This suite tests whether the harness, followed faithfully, produces principal-grade
delivery artifacts for Financial Services work.

## Method (fixed before any run)

1. **Ground truth first.** For each scenario, `ground-truth/*.yaml` defines the
   expected outcome as scorable checks (MUST/SHOULD), written before any run and
   frozen. Checks encode what a principal engineer in a regulated institution would
   demand — deliberately including things the harness might not yet prompt for.
2. **Faithful runs.** Artifacts in `runs/<scenario>/run-N/` are produced strictly
   from the harness's templates and skill instructions — nothing added from operator
   knowledge that the harness didn't ask for. This measures what the harness
   *elicits*, the same way you test a checklist by following only the checklist.
3. **Mechanical scoring.** `score.py <ground-truth> <run-dir>` regex-checks each
   artifact. No self-grading judgment in the pass/fail.
4. **Iterate on the harness, not the answers.** A failed check is a harness gap:
   fix the template/skill that should have elicited it, then produce run-N+1 from
   the improved harness. Never edit a run artifact to pass a check directly.

## Satisfactory bar

- MUST checks: **100%**
- SHOULD checks: **≥ 80%**

## Scenarios

| Scenario | Path | What it stresses |
| --- | --- | --- |
| Greenfield: payment-exception triage with AI classification | `scenarios/greenfield-payment-triage.md` | Full path G0→G3: tiering, PII-in-prompts, eval specs, HIL, threat model, planning, issues |
| Brownfield: interest-rounding drift in a legacy statement generator | `scenarios/brownfield-rounding-drift.md` | Fast path: ticket repair, recon, Hyrum contracts, escalation triggers, remediation of past impact |
| Model upgrade under deprecation deadline | `scenarios/model-upgrade-triage.md` | Operate-phase re-entry: offline floors, shadow cutover, pre-decided deadline rule |
| Break-glass: actively exploited RCE | `scenarios/breakglass-cve.md` | Gate GE: time-ordered evidence, interim mitigation, compromise assessment |
| Regulatory-report restatement (issue #2) | `scenarios/regreport-restatement.md` | Effective-dating by period, parallel run, restatement disposition, control totals |
| Vendor integration (issue #3) | `scenarios/vendor-screening.md` | Third-party risk: data leaving the estate, TPRM, fail-closed as a named decision, exit plan |

## Run

```bash
.venv/bin/python evals/harness/score.py evals/harness/ground-truth/greenfield.yaml evals/harness/runs/greenfield/run-1
.venv/bin/python evals/harness/score.py evals/harness/ground-truth/brownfield.yaml evals/harness/runs/brownfield/run-1
```

Results and the fix log live in `REPORT.md`.

## Reproducibility (issue #4)

The regression is code, not habit:

- `manifest.yaml` pins each scenario's frozen ground truth to its **accepted run**.
- `tests/test_harness_evals.py` scores every manifest entry via the same `score.py`
  CLI — so `pytest`, the local verify loop, and CI all reproduce identical scoring.
  A guard test fails if a ground truth exists without a manifest entry.
- `.github/workflows/verify.yml` runs `scripts/verify.sh` (typecheck, lint, tests
  including this regression) plus a full-history gitleaks scan on every push/PR.
- Frozen ground truths are never edited to make a run pass; scorer-regex lessons in
  `REPORT.md` apply to *future* GTs only.

## Reproducing a run / adding a scenario (blind-run protocol)

Designed for ground truths authored by someone other than the run author — the
strongest form of this eval:

1. **Author** writes `scenarios/<name>.md` (the brief: facts an operator could
   discover) and `ground-truth/<name>.yaml` (frozen checks). The GT is not shown
   to whoever produces the run.
2. **Runner** (human + LLM pair) produces `runs/<name>/run-1/` strictly from the
   harness's templates and skills applied to the brief — no peeking at the GT,
   nothing added that the harness didn't elicit.
3. Score: `.venv/bin/python evals/harness/score.py ground-truth/<name>.yaml runs/<name>/run-1`.
4. Failures → fix **templates/skills**, never run artifacts; produce `run-2` from
   the improved harness; rescore until SATISFACTORY.
5. Add the accepted run to `manifest.yaml` — from then on CI holds the line.
