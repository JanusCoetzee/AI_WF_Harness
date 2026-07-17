# Gates

A gate is passed when (a) every evidence item exists in the repo, (b) the named human
approves, and (c) a line is appended to `docs/harness/DECISIONS.log`. `scripts/gate-check.sh <gate>`
verifies (a) mechanically. Which gates apply depends on risk tier (`harness.config.yaml`).

**Skipping a gate is an incident, not a shortcut.** Overrides are allowed — logged, with a reason.

Two entry paths share the back half of the pipeline:

- **Greenfield / project-sized:** G0 → G1 → G2 → G3 → build → G4 → G5 → G6 → G7.
- **Brownfield fast path** (most day-to-day work on existing code): **GC** replaces
  G0–G3, then rejoins at build → G4 → G5 → G6 → G7 per tier. See stages B0/B1.
  Any tripped escalation trigger in `CHANGE.md` exits the fast path into the full
  workflow at the gate named there.

## GC — Change Ratified (brownfield fast path; replaces G0–G3)

| | |
| --- | --- |
| Evidence | `docs/harness/changes/CHG-###/CHANGE.md`: named source, tier with rationale, testable `CHG-###.n` acceptance criteria, blast radius, rollback note, all four escalation triggers answered; `RECON.md` with code map (file:line cited), consumer inventory, implicit-contract table, and **characterization tests green against unchanged code** — recon waivable only for docs/typo-level trivia, waiver written in CHANGE.md |
| Approver | Driver (T2/T3); Driver + one peer (T1) |
| Fails if | Any blast-radius row reads "unknown"; an escalation trigger is "yes" but not escalated; touched path has thin coverage and no characterization tests; behavior claims without file:line evidence |

After GC: standard pipeline from Stage 04 — G4, G5, G6, G7 apply per tier.

**Maintenance lane** (routine hygiene): one `MAINT-YYYY-MM` batch dossier
(`templates/MAINTENANCE.md`) reuses GC — the batch's changelog review + green
verify + clean audit stands in for per-package recon; majors and sensitive
libraries eject to individual changes. `gate-check.sh GC MAINT-YYYY-MM` applies.

## GE — Break-glass (emergency; time-ordered inversion of the pipeline)

| | |
| --- | --- |
| Trigger | ONLY: exploit in the wild / active customer harm / hard external deadline — declared by a **named human with authority**, never self-invoked by the AI |
| At the time | `BREAK-GLASS.md` Part A filled as the fix happens: authorizer, peer eyes, smallest-scope fix, verify evidence (degradation disclosed, never zero), rollback, DECISIONS.log entry at deploy time |
| Within 2 business days | Part B: retrospective CHANGE/RECON, undegraded verify, retrospective G5 review + G6 scans, retroactive change record, and a retro answering: justified? if the normal path was too slow for legitimate work, what gets fixed in the path? |
| Fails if | Documented after the fact; invoked for convenience; Part B misses its deadline (that's an incident); the same justified trigger recurs without a path fix |

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
| Evidence | `PLAN.md`: milestones each ending runnable with a stated **demo command**; tasks ≤ half a day; every task maps to `REQ-###`; test strategy per milestone; where a ticketing system is in use, tasks externalized as issues meeting the **Definition of Ready** (`templates/ISSUE.md`) with ticket keys written back into PLAN.md |
| Approver | Driver |
| Fails if | A milestone has no demo; a task is "misc" or unmapped; plan exceeds ~2 weeks without a re-planning checkpoint |

## G4 — Build Verified (Build → Review)

| | |
| --- | --- |
| Evidence | Verify loop green (`scripts/verify.sh` output committed to `docs/harness/evidence/`); **standards thresholds met** (`docs/STANDARDS.md`: changed-line coverage, mutation score, complexity ceiling); eval scores ≥ thresholds; every milestone demo recorded (command + observed result in PLAN.md); no `UNVERIFIED` items outstanding |
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
| Evidence | Secret scan clean (STD-005); dependency audit at the STD-004 severity gate — no High/Critical, or waivers with expiry + owner; threat-model delta reviewed against what was actually built; data-handling confirmed (no real data in fixtures/logs); change record raised (T1/T2) |
| Approver | Risk/Sec partner (T1); Driver with checklist (T2) |
| Fails if | Any Critical/High finding unremediated and unwaived |

## G7 — Released & Observed (Release → Operate)

| | |
| --- | --- |
| Evidence | Evidence bundle built (`scripts/evidence-bundle.sh`); rollback plan tested (not just written); progressive rollout completed with health checks (T1); dashboards/alerts live; release approver sign-off |
| Approver | Release approver |
| Fails if | Rollback is a theory; "we'll add monitoring later" |
