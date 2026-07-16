# CHANGE — CHG-### <title>

One page, no more. If this document wants to grow, that's an escalation trigger, not
a formatting problem.

| Field | Value |
| --- | --- |
| Status | Draft / **Ratified (GC)** / Escalated to full workflow / Done |
| Driver | |
| Source (ticket / requester — named) | |
| Date | |
| Risk tier | T_ — <rationale: money movement? data above Internal? regulatory? blast radius?> |
| Recon | required / waived-trivial (docs/typo-level only; waiver reason: ___) |
| Linked records | <audit findings, incidents, regulatory items this change closes or touches — e.g. AUD-####-###; "none" only after checking> |
| Timing constraints | <freeze windows, batch/statement cycles, reporting deadlines that gate when this may deploy> |

## Intent

Two sentences max: what's wrong or wanted, and what "done" looks like for the requester.

## Acceptance criteria

Testable as written. Commits, tests, and the PR reference `CHG-###`.

| # | Given / When / Then |
| --- | --- |
| CHG-###.1 | |
| CHG-###.2 | |

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | |
| Known consumers of touched behavior | |
| Data elements involved + classification | |
| Deploy surface (config, migration, infra?) | |

## Rollback note

How this change is undone if it's wrong. "Revert the commit" is acceptable only if
there is no migration, no config change, and no consumer that adapts.

## Remediation of past impact

A fix changes the future; a bank also answers for the past. If the defect produced
wrong figures, documents, reports, or customer outcomes before the fix: what is the
disposition of the historical impact (restate / back-fill / customer communication /
write-off closure / regulator notice / accepted as-is with owner)? "Forward-only"
is a decision — name who made it.

## Escalation triggers — answer all four honestly

Any "yes" exits the fast path into the full workflow at the gate named.

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | | G2 (threat model + ADR) |
| Decision that deviates from the existing pattern in this codebase? | | ADR required before build |
| Effort beyond ~3 days after recon? | | G1 (full PRD) |
| Tier raised during recon? | | Re-approve intake at new tier |

## GC sign-off

T2/T3: Driver. T1: Driver + one peer on the intake itself.
Record in `DECISIONS.log`: `<date> | GC passed | <who> | CHG-###`
