# CHANGE — GH-21 concrete revisit triggers for ADR-008's two accepted risks

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #21 — found compiling a follow-up backlog after GH-16, originally flagged 2026-07-25 |
| Date | 2026-08-12 |
| Risk tier | T3 — documentation only (threat-model table content), no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level: reads two existing artifacts already cited by the ticket — `docs/harness/changes/GH-8/THREAT-MODEL.md` and `docs/harness/adr/ADR-008-independent-bu-instances.md` — and edits one table's two rows) |
| Linked records | ADR-008 (2026-07-25, `DECISIONS.log`); GH-8's `THREAT-MODEL.md` Assumptions & accepted risks table, rows 6-7 |
| Timing constraints | none |
| Constitution sections consulted | §5 (traceability — accepted risks without a revisit trigger quietly become permanent ones), §8 (retroactive documentation only for what's touched — closes exactly this gap, no wider archaeology) |

## Intent

`THREAT-MODEL.md`'s risks #6 (governance-only drift control) and #7 (cross-BU
leak via shared skill namespace, unmitigated) were logged "pending revisit
triggers" with no actual trigger named — no date, volume threshold, incident
type, or BU count. Done means both rows carry a concrete, named condition
that would actually prompt someone to revisit, written into the table itself.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-21.1 | Risk #6's row states a named, checkable trigger (severity + time threshold, an instance-count threshold, and an incident-type condition — first to fire wins) rather than a vague "if a stale instance is found" |
| GH-21.2 | Risk #7's row states a named, checkable trigger (a BU-count threshold, and an explicit tie to #11 MCP's design if it turns out relevant) |
| GH-21.3 | Where a real mitigation is now obvious given how #9/#10 landed, it's proposed in the row, not just a trigger — done: a `classification` field proposal for #10's still-in-progress manifest schema, addressing risk #7 |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `docs/harness/changes/GH-8/THREAT-MODEL.md` only (one table, two rows) |
| Known consumers | humans doing G6 delta-review of GH-8/ADR-008; whoever eventually decides #10's manifest schema (the GH-21.3 proposal is a recommendation for that person, not a mandate — this ticket doesn't touch code) |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit. No migration, no consumer that parses this table programmatically.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — states triggers for risks the threat model already accepted; the GH-21.3 mitigation proposal is a recommendation for #10 to pick up or reject, not a decision made here | ADR |
| Effort beyond ~3 days after recon? | No — under an hour | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-12 | GC passed | janus | GH-21`
