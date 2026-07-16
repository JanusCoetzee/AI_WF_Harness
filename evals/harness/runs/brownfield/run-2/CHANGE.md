# CHANGE — OPS-2214 Statement interest matches ledger (rounding alignment)

| Field | Value |
| --- | --- |
| Status | Ratified (GC) — drill |
| Driver | janus |
| Source (ticket / requester — named) | OPS-2214, b.naidoo (Ops Reconciliation) — ticket repaired to standard first (ticket-repair.md) |
| Date | 2026-07-17 |
| Risk tier | T1 — customer-facing statement figures, audit finding attached, tax-reporting feed downstream |
| Recon | required |
| Linked records | **AUD-2026-041** (internal audit finding on recurring recon write-offs — this change is the remediation; closure evidence = replay proof + retired journal); OPS recon journal entries (retire) |
| Timing constraints | Statement run on 1st business day of month with a 2-business-day change freeze around it — deploy no later than BD-3 of the target cycle, or wait a cycle |

## Intent

Statement interest drifts from the ledger by cents because stmtgen rounds per daily
line HALF_UP while the ledger rounds once monthly HALF_EVEN. Done means regenerated
statements match the ledger to the cent with no other figure changing.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| OPS-2214.1 | Masked replay of last closed cycle → every interest figure equals ledger to the cent |
| OPS-2214.2 | Known drift accounts → differences become zero |
| OPS-2214.3 | Zero-drift accounts → figures byte-identical (no collateral movement) |

## Blast radius (estimate — recon confirms or corrects)

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | stmtgen AccrualAggregator (rounding site only) |
| Known consumers of touched behavior | customer PDF statements; GL reconciliation export; tax-reporting feed (recon to confirm exact coupling) |
| Data elements involved + classification | statement interest amounts — Confidential; test env masked data only |
| Deploy surface (config, migration, infra?) | code only |

## Rollback note

Revert alone is insufficient for anything already generated: statements, once
dispatched, cannot be unsent, and the GL export for a run is consumed same-day.
Rollback = revert commit + regenerate any not-yet-dispatched batch; anything
dispatched under the bad build is an incident, not a rollback.

## Remediation of past impact

The defect has produced drifted figures on issued statements and in submitted tax
feeds for years. Disposition, decided with Finance (not silently):

- **Issued statements:** no restatement — differences are ±3 cents, below the
  restatement materiality threshold; Finance to confirm and own the ruling in
  writing (blocks release).
- **Prior tax feeds:** Finance ruling required on whether prior-year submissions
  need correction or fall under the de-minimis policy; this change does not deploy
  until that ruling is recorded.
- **Historical write-offs:** recon journal history retained as the audit trail;
  AUD-2026-041 closure pack references it.
- Forward-only code fix is the decision *for the software*; the past is dispositioned
  above with named owners.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — same outputs, corrected values | G2 |
| Decision that deviates from the existing pattern in this codebase? | **Yes — changing the rounding mode/site is an accounting-policy-significant decision; the incumbent HALF_UP is undocumented. ADR required before build** (adr/ADR-001-rounding.md) | ADR before build |
| Effort beyond ~3 days after recon? | No — the fix is small; the replay proof is the work | G1 |
| Tier raised during recon? | No — entered at T1 | re-approve |

## GC sign-off

T1: Driver + one peer on the intake itself. Record in DECISIONS.log.
