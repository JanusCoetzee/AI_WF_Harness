# Review Record — CHG-114 (G5)

## Reviewer pack (prepared by the AI pair)

| Field | Value |
| --- | --- |
| Change | CHG-114 — idempotency-key support for `POST /api/payments/retry` (`paysvc`) |
| Commit under review | 8f2c1a9 |
| REQs served | REQ-091, REQ-092, REQ-093 (PRD.md, G1-passed) |
| Evidence | verify log — 19 passed, coverage 91%, `verify: ALL GREEN` @ 8f2c1a9, 2026-06-18T14:02:11Z |
| Demo | not provided in the PR materials handed to this review — **flag: no demo instructions attached** |
| Diff size | 612 changed lines (`app/paysvc/retry.py` ~340, `tests/test_retry.py` ~210, `migrations/0007_idempotency_key.py`) — **exceeds the ~500-line ceiling (GATES.md G5 / SKILL step 4)** |
| Tier | T1 (money movement) — requires 2 human reviewers |
| Area of least confidence (PR author's own statement) | "none — straightforward CRUD-shaped feature" |
| Area of least confidence (this review's assessment) | The check-then-act window between the idempotency-key lookup and the insert, and what `charge_gateway.retry()` does if it raises — neither is exercised by the attached tests or visible in the diff excerpt |

## AI adversarial self-review (input to G5 — approves nothing)

Hunted for: plausible-but-wrong, test theater, invented APIs, unvalidated
boundaries, REQ drift, weakened assertions. Findings ranked:

| # | Severity | Finding | Failure scenario | Disposition |
| --- | --- | --- | --- | --- |
| 1 | **Critical** | Check-then-act race in `retry.py:41-58`: the idempotency lookup (line 47) and the insert/commit (lines 53-54) are not atomic — no `SELECT ... FOR UPDATE`, no `try/except IntegrityError` around the insert, despite the migration adding a unique index on `idempotency_key` that would catch the collision if the app actually handled it | Production load pattern stated in the brief: an automatic client retry-on-timeout policy fires two requests carrying the *same* `Idempotency-Key` within milliseconds under gateway latency spikes. Both requests can pass the line-47 lookup (neither sees the other's row yet), both proceed to call `charge_gateway.retry(payment_id)` at line 53 — and `charge_gateway.retry()` is explicitly stated to be **not idempotent on the gateway side**. Result: two real charges for one logical retry, which is the exact outcome REQ-091 ("performs no new charge") exists to prevent. The unique index would raise `IntegrityError` on the second insert, but nothing in `retry.py` catches it — that request either 500s after a real charge already fired, or (worse, unverifiable from the excerpt) the exception path is untested | **Must fix before merge**: wrap the insert in `try/except IntegrityError`, or take a row lock / use `INSERT ... ON CONFLICT` semantics, before the charge call — not after |
| 2 | **High** | Test theater in `test_duplicate_key_returns_cached_response` (`tests/test_retry.py:88-101`): the two requests are issued **sequentially**, not concurrently, so the test always exercises the safe "row already committed" path, never the race window that finding 1 describes. The test file itself carries a comment acknowledging the gap: `# (no assertion on charge_gateway.retry call count)` | This test passes today and would keep passing even if concurrent duplicate requests double-charge in production — coverage (91%) and "19 passed" give false confidence on the one behavior (REQ-091's "no new charge") that most needs verifying. A reviewer who only reads the green verify log, not the test body, would not catch this | **Must fix before merge**: add a concurrency-shaped test (two near-simultaneous requests against a shared session/thread) asserting `charge_gateway.retry` is called at most once, not just that the second response matches the first |
| 3 | **High** | PR states "Area of least confidence: none — straightforward CRUD-shaped feature" for a T1 money-movement change that in fact has a live TOCTOU race against a non-idempotent external gateway | This statement is itself a signal the author didn't identify the race — it's exactly the kind of self-assessment G5 exists to catch before it reaches human reviewers as an implicit "nothing to look at here" | Reviewer should not accept this framing at face value; direct human attention specifically to `retry.py:41-58` regardless of the author's stated confidence |
| 4 | Medium | REQ-093 requires each audit-log entry to carry "the key, outcome, **and timestamp**." The three `audit_log.write(payment_id, idempotency_key, outcome)` call sites shown in the excerpt pass only payment_id, key, and outcome — no timestamp argument is visible | If `audit_log.write` doesn't stamp time internally (not evidenced either way in the diff excerpt handed to this review), REQ-093's acceptance criterion is not met, and no test in the excerpt asserts a timestamp field on the written record | Cannot resolve from the material given — reviewer must open `audit_log.write`'s definition; flagged as a REQ-093 trace gap, not confirmed pass or fail |
| 5 | Medium | No exception handling around `charge_gateway.retry(payment_id)` (line 53, called on the external processor). If it raises, the request has no audit-log entry, and REQ-093's "every retry attempt (accepted or rejected)" invariant is broken for that attempt — the code never reaches the line-56 `audit_log.write(..., "processed")` call, and there is no `except` branch that would log a failure outcome | An external processor timeout or 5xx mid-request leaves the retry attempt completely unaudited — the opposite of what an audit trail is for on a T1 money-movement endpoint | Should fix: wrap the gateway call, log a "gateway_error" (or similar) outcome on failure, decide (and document) whether the DB insert should also be rolled back in that path |
| — | — | Checked and clean, within what the brief provides: the 400-rejection path (REQ-092) matches the excerpt at `retry.py:41-44`; no invented APIs are visible in the excerpt (ORM `.query.filter_by().first()` and `db.session` usage are unremarkable SQLAlchemy patterns, though the pinned dependency version wasn't available to check against); no unrelated hunks are apparent from the diff summary (all three files map to CHG-114) | | |

## Traceability spot-check (full trace — REQ-091/092/093, per ADR-005)

| REQ | Acceptance criterion | Walks to | Result |
| --- | --- | --- | --- |
| REQ-091 | Previously-seen key returns original response, no new charge | Code: `retry.py:47-51` (lookup + return cached). Test: `test_retry.py:88-101` | **Break.** The "no new charge" half of the criterion is unverified — no assertion on `charge_gateway.retry` call count — and unguaranteed under concurrency by the code itself (finding 1). Response-matching half is covered. |
| REQ-092 | Missing key rejected with 400 | Code: `retry.py:41-44` — matches the criterion directly | **No break found in code.** No corresponding test is visible in the material handed to this review (only the duplicate-key test excerpt was provided); reviewer cannot confirm test coverage of this branch from the brief alone — flagged as a visibility gap, not a code defect. |
| REQ-093 | Every attempt (accepted or rejected) writes one audit entry with key, outcome, timestamp | Code: `retry.py:35, 39, 56` (three `audit_log.write` call sites) | **Break.** Covers the three branches shown, but (a) timestamp field not evidenced in the call signature (finding 4), and (b) the unhandled-exception path from `charge_gateway.retry()` produces zero audit entries, violating "every retry attempt" (finding 5). |

3 of 3 REQs traced; 2 of 3 show a break, 1 has a visibility gap this review
could not close from the material provided.

## Gate/process findings (not code defects — G5 evidence gaps)

- **Reviewer count**: T1 requires 2 human reviewers (GATES.md G5). Only
  `t.owens` is listed as approved; no second reviewer named. G5 evidence is
  incomplete as-is.
- **Diff size**: 612 changed lines exceeds the ~500-line ceiling GATES.md and
  SKILL.md step 4 both flag as a rubber-stamp risk for a single sitting.
  Recommend splitting — e.g., migration + idempotency-record model in one PR,
  endpoint logic + tests in a second — before the second human review proceeds.
- **AI approval counts for nothing** (GATES.md G5): the above is input to
  human reviewers, not a substitute for their sign-off.

## Human review (T1: two reviewers required)

| Reviewer | Verdict | Date |
| --- | --- | --- |
| t.owens | Approve (per PR) — **recorded before this self-review; findings 1–5 above were not evidently addressed at the time of that approval** | (date not given in brief) |
| *(second T1 reviewer)* | **Not yet obtained — pending.** This is a drill run; no human reviewed this material in this session. G5 cannot pass without a second, independent T1 reviewer. | — |

**G5 status: NOT PASSED.** Blocking on: (1) a second T1 human reviewer, (2)
disposition of findings 1–2 (Critical/High, code-level) before re-review, (3)
a decision on whether to split the PR given the 612-line diff.
