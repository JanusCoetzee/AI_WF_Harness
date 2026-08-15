# CHANGE — GH-17 req-trace.sh never recognizes GH-##.# ticket-key IDs

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #17 — found compiling a follow-up backlog after GH-16, 2026-08-12 |
| Date | 2026-08-12 |
| Risk tier | T2 — internal governance tooling (G5 evidence quality); no customer data, no external interface |
| Recon | waived-trivial (single-line regex swap in a script with no test harness; behavior fully characterized by re-running the script before/after against the live repo, pasted below) |
| Linked records | none pre-existing |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop — standards are failing conditions), §5 (traceability — gate evidence must actually attest the work), §8 (brownfield — cite file:line, understand before changing) |

## Intent

`scripts/req-trace.sh`'s `collect_ids()` only matched `REQ-###`/`CHG-#`,
so it silently never traced any `GH-##.#`-keyed acceptance criterion — the
ID shape this repo's own tickets actually use per CLAUDE.md §5. Done means
the collector recognizes the same broad ticket-key shape
`scripts/hooks/commit-guard.sh` already accepts.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-17.1 | Given `docs/harness/changes/*/CHANGE.md` files with `GH-<n>.<m>` acceptance-criteria IDs, when `req-trace.sh` runs, then every such ID appears as a row in the trace table (previously: none did) |
| GH-17.2 | Given the existing `REQ-###`/`CHG-#` shapes, when `req-trace.sh` runs, then they are still collected and traced identically to before (no regression) |
| GH-17.3 | The widened regex matches `scripts/hooks/commit-guard.sh`'s broader ticket-key pattern (`[A-Z][A-Z0-9]{1,9}-[0-9]+`), extended with the optional `.n` suffix `commit-guard.sh` doesn't need |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/req-trace.sh` only (one regex in `collect_ids()`) |
| Known consumers | humans running `req-trace.sh` manually at G5 (per `gates/GATES.md`'s G5 evidence line); **not** wired into `scripts/verify.sh` or CI (`grep -rn req-trace scripts/verify.sh .github/workflows` — no hits), so this cannot regress CI |
| Data elements | none — reads local markdown, Internal at most |
| Deploy surface | script only |

## Remediation of past impact

This changes what previously-silent G5 evidence would have shown for every
GH-keyed work item to date (GH-6, GH-8, GH-12 through GH-16): running the
fixed script now surfaces real, previously-invisible gaps — e.g. `GH-12.1`,
`GH-12.2`, `GH-12.3`, `GH-13.1..3`, `GH-15.1..3` currently trace to nothing
across ADR/PLAN/tests/commits. Checked `DECISIONS.log`: no G5 passage for
those items cited a `req-trace.sh` run as its evidence (the manual "pick 3
REQs" spot check ADR-005 replaced was what ran instead, informally, before
this script existed for GH-keyed items). Disposition: forward-only fix; the
now-visible gaps are noted here as **found**, not retroactively re-opening
those items' gates — a human call on whether any need real follow-up
(separate from this ticket, which only fixes the detector).

## Rollback note

Revert the commit. No migration, no consumer that depends on the narrower regex.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — matches `commit-guard.sh`'s existing broader pattern, doesn't invent a new one | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## Verification (manual — no test harness for this bash script)

```
$ bash scripts/req-trace.sh | head -3
req-trace: ✗ 10 id(s) with zero hits across ADR/PLAN/tests/commits
| ID | ADR | PLAN | tests | commits |
| --- | --- | --- | --- | --- |
```
GH-##/GH-##.# rows now present (previously entirely absent); REQ-###/CHG-#
rows still present and unchanged. The 10 zero-hit ids are real, pre-existing
gaps this fix newly surfaces — see "Remediation of past impact" above.

## GC sign-off

T2: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-12 | GC passed | janus | GH-17`
