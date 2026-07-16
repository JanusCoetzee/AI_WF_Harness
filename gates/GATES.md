# Gates

A gate is passed when (a) every evidence item exists in the repo, (b) the named human
approves, and (c) a line is appended to `docs/harness/DECISIONS.log`. `scripts/gate-check.sh <gate>`
verifies (a) mechanically. Which gates apply depends on risk tier (`harness.config.yaml`).

**Skipping a gate is an incident, not a shortcut.** Overrides are allowed — logged, with a reason.

## G0 — Idea Approved (Ideate → Discover)

| | |
| --- | --- |
| Evidence | `docs/harness/IDEA.md`: problem statement, who hurts today, why now, kill criteria; **risk tier assigned with rationale** |
| Approver | Driver (self, logged) — T1 additionally needs a sponsor named |
| Fails if | The idea is a solution wearing a problem costume; no kill criteria |

## G1 — Requirements Locked (Discover → Architect)

| | |
| --- | --- |
| Evidence | `PRD.md` with numbered `REQ-###` and testable acceptance criteria; explicit **non-goals**; data classification of every data element touched |
| Approver | Driver + product/business owner (T1) |
| Fails if | Any requirement is untestable as written; data classification missing |

## G2 — Design Approved (Architect → Plan)

| | |
| --- | --- |
| Evidence | ADR(s) for significant decisions, **each showing ≥2 options considered**; threat model (full STRIDE for T1, boundary table for T2); `EVAL-SPEC.md` for every AI-powered behavior, thresholds agreed |
| Approver | Driver + Risk/Sec partner (T1); Driver (T2) |
| Fails if | Single-option ADRs; AI feature without eval thresholds; unmodeled trust boundary |

## G3 — Plan Ratified (Plan → Build)

| | |
| --- | --- |
| Evidence | `PLAN.md`: milestones each ending runnable with a stated **demo command**; tasks ≤ half a day; every task maps to `REQ-###`; test strategy per milestone |
| Approver | Driver |
| Fails if | A milestone has no demo; a task is "misc" or unmapped; plan exceeds ~2 weeks without a re-planning checkpoint |

## G4 — Build Verified (Build → Review)

| | |
| --- | --- |
| Evidence | Verify loop green (`scripts/verify.sh` output committed to `docs/harness/evidence/`); eval scores ≥ thresholds; every milestone demo recorded (command + observed result in PLAN.md); no `UNVERIFIED` items outstanding |
| Approver | Driver |
| Fails if | Tests weakened to pass; coverage on changed lines regressed; demo skipped |

## G5 — Review Passed (Review → Secure)

| | |
| --- | --- |
| Evidence | Human review approval(s) per tier (T1 = 2, T2 = 1); AI adversarial self-review attached as *input*; traceability spot-check (pick 3 REQs, walk them to code+tests); review record in `docs/harness/` |
| Approver | Reviewer(s) — **must not be the Driver; AI approval counts for nothing** |
| Fails if | Reviewer rubber-stamps > ~500 changed lines in one sitting — split the PR |

## G6 — Security & Compliance Cleared (Secure → Release)

| | |
| --- | --- |
| Evidence | Secret scan clean; dependency audit clean or exceptions logged; threat-model delta reviewed against what was actually built; data-handling confirmed (no real data in fixtures/logs); change record raised (T1/T2) |
| Approver | Risk/Sec partner (T1); Driver with checklist (T2) |
| Fails if | Any Critical/High finding unremediated and unwaived |

## G7 — Released & Observed (Release → Operate)

| | |
| --- | --- |
| Evidence | Evidence bundle built (`scripts/evidence-bundle.sh`); rollback plan tested (not just written); progressive rollout completed with health checks (T1); dashboards/alerts live; release approver sign-off |
| Approver | Release approver |
| Fails if | Rollback is a theory; "we'll add monitoring later" |
