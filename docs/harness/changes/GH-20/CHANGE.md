# CHANGE — GH-20 audit-decisions.sh doesn't cross-check "closed" claims against actual GitHub issue state

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #20 — found during independent re-verification of GH-16, 2026-08-12 |
| Date | 2026-08-12 |
| Risk tier | T2 — internal governance tooling; runs inside `verify.sh`'s lint step, but degrades gracefully (best-effort, network-dependent) rather than hard-failing CI/offline runs |
| Recon | waived-trivial (additive check appended to an existing, well-understood script; new external dependency — `gh` CLI — is already a first-class tool in this repo's own tickets/DECISIONS.log, not a new one being introduced) |
| Linked records | GH-19 (same script, same session's finding, chronology check landing alongside this one); the GH-16 misdated "closed" claim this generalizes from |
| Timing constraints | none |
| Constitution sections consulted | §2 (verify loop, but explicitly: "if you cannot run verification... say so and mark UNVERIFIED" — this check follows that same discipline by skipping-with-warning rather than failing when `gh` is unavailable), §5 (traceability) |

## Intent

A session working GH-16 wrote `DECISIONS.log`/`STATE.md` entries claiming
"GH-16 closed" while — correctly, per that session's own constraint — it had
not run `gh issue close`; the issue was genuinely still open. Nothing in the
repo checked an *external* claim like this. Done means `audit-decisions.sh`
best-effort cross-checks `#<n> closed`/`GH-<n> closed`-shaped claims in
`DECISIONS.log`/`STATE.md` against `gh issue view <n> --json state`, skipping
(not failing) when `gh` isn't installed/authenticated.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-20.1 | Given a `DECISIONS.log`/`STATE.md` line claiming `#<n> closed` (or `GH-<n> closed`) for an issue that `gh issue view <n>` reports as `OPEN`, when `audit-decisions.sh` runs with `gh` available and authenticated, then it fails and names the issue number and the actual state |
| GH-20.2 | Given the same claim for an issue actually `CLOSED` on GitHub, when the check runs, then it passes |
| GH-20.3 | Given `gh` not installed or not authenticated, when the check runs, then it prints a skip warning and does not fail the script (best-effort, per the ticket's own scoping) |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `scripts/audit-decisions.sh` only (new section 6, appended) |
| Known consumers | `scripts/verify.sh` lint step (every verify run, local + CI); humans running the script directly |
| Data elements | none — issue numbers and open/closed state only, no content fetched or logged |
| Deploy surface | script only; adds a runtime dependency on `gh` CLI + network reachability to github.com, degraded gracefully per GH-20.3 |

## Rollback note

Revert the commit. Purely additive; no existing check's logic changed.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No — reads public issue metadata via an already-installed CLI, no new network surface the repo doesn't already use (`gh` is used interactively throughout this session and prior ones) | G2 |
| Decision that deviates from the existing pattern? | No — same `require_line`-style "scan, count FAILS, report" pattern as sections 1-5; the graceful-degradation-when-unavailable pattern mirrors CLAUDE.md §2's own UNVERIFIED discipline | ADR |
| Effort beyond ~3 days after recon? | No — under an hour | G1 |
| Tier raised during recon? | No | re-approve |

## Verification (manual — no test harness for this bash script)

```
$ bash scripts/audit-decisions.sh          # clean run, gh authenticated
  ~ no '#<n> closed' claims found
audit-decisions: all claims logged.

# injected a false claim: "GH-17 closed for testing purposes" (GH-17 is open)
  ✗ #17 claimed closed in docs/harness/DECISIONS.log/STATE.md but GitHub reports OPEN
audit-decisions: FAIL (1 unlogged/inconsistent claim(s)) — log them or retract the claims.
```
Injected line reverted immediately after; `git diff docs/harness/DECISIONS.log` clean.
`gh auth status` confirmed authenticated for this run (`JanusCoetzee`, keyring).

## GC sign-off

T2: Driver approval still needed (session constraint: no gate self-approval, no push/close without checking with the Driver first). On approval, log: `2026-08-12 | GC passed | janus | GH-20`
