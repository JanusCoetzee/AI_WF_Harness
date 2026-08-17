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
| Constitution sections consulted | <CLAUDE.md §s relevant to this change, e.g. "§8 brownfield, §5 traceability"> |

**T3 shortcut (ADR-010):** if risk tier is T3, collapse **Linked records**,
**Timing constraints**, and the **Regulated / reported outputs** section below
into one line — `Regulatory/audit surface: none (T3 — see harness.config.yaml)`
— unless something in scope is actually reportable, in which case answer the
fields in full as normal. T1/T2 always answer them in full; a T3 change later
promoted to T1/T2 must re-expand this line back into the full fields.

## Intent

Two sentences max: what's wrong or wanted, and what "done" looks like for the requester.

**If this change produces a user-facing document or artifact** (report, page, PDF,
printed material, dashboard, ...): state its delivery medium / consumption context
explicitly here — screen-only, print, mobile, offline/printed binder, etc. An
acceptance criterion that hedges between formats ("X lints clean **or** Y validates")
is the tell that this question was never actually answered — resolve it here, before
GC, not by letting the hedge stand in for a decision (CLAUDE.md §9).

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

## Regulated / reported outputs (delete section only if nothing here feeds a regulator, tax, or financial report)

| Question | Answer |
| --- | --- |
| **Parallel run**: at least one cycle produced under old AND new logic, deltas explained, before the first live submission? | |
| **Control total**: what mechanically proves no records were lost/double-counted between source and report? | |
| **Lineage**: is each reported figure traceable to the rule/code version and source data that produced it? | |
| **Accountable owner sign-off**: the report's business signatory approves the change — engineering peers are not enough for a regulated output | |

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
