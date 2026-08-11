# Scenario: paysvc — idempotent payment retry (Stage 05 / G5 review)

*Input handed to the harness: a completed build ready for review — diff summary,
verify evidence, and the REQ list it serves. The runner produces only
`review-record.md` from `/harness-review`, strictly from harness skill
instructions. Fictional but representative; facts below are what a reviewer could
discover from the diff, the repo, and the PR description — nothing more.*

## Work item

`CHG-114` — add idempotency-key support to `POST /api/payments/retry` in
`paysvc` (Python, Flask), a T1 service (money movement). Locked REQs from
`PRD.md` (already G1-passed, not part of this scenario):

| REQ | Acceptance criteria |
| --- | --- |
| REQ-091 | A retry request with a previously-seen `Idempotency-Key` returns the original response and performs no new charge. |
| REQ-092 | A retry request missing `Idempotency-Key` is rejected with `400`. |
| REQ-093 | Every retry attempt (accepted or rejected) writes one audit-log entry with the key, outcome, and timestamp. |

Tier: **T1** (money movement) — two human reviewers required.

## Diff summary (as the reviewer would see it in the PR)

`app/paysvc/retry.py` (new endpoint, ~340 lines) + `tests/test_retry.py` (new,
~210 lines) + `migrations/0007_idempotency_key.py` (new column + unique index).
**Total diff: 612 changed lines.**

Key excerpt, `app/paysvc/retry.py:41-58`:

```python
def retry_payment(payment_id, idempotency_key):
    if not idempotency_key:
        audit_log.write(payment_id, idempotency_key, "rejected_missing_key")
        return error_response(400, "Idempotency-Key required")

    existing = IdempotencyRecord.query.filter_by(key=idempotency_key).first()   # line 47
    if existing:
        audit_log.write(payment_id, idempotency_key, "duplicate_returned")
        return existing.cached_response

    result = charge_gateway.retry(payment_id)                                   # line 53
    db.session.add(IdempotencyRecord(key=idempotency_key, cached_response=result))
    db.session.commit()
    audit_log.write(payment_id, idempotency_key, "processed")
    return result
```

`migrations/0007_idempotency_key.py`: adds `idempotency_key` column with a
**unique index** to `idempotency_records` — present in the migration, but
`retry.py:41-58` never relies on it; the code path is check-then-act (query at
line 47, insert at line 54) with no `try/except IntegrityError` around the
insert and no row-level lock.

`tests/test_retry.py:88-101` (the retry-twice test):

```python
def test_duplicate_key_returns_cached_response():
    r1 = client.post("/api/payments/retry", json={"payment_id": "p1"},
                      headers={"Idempotency-Key": "k1"})
    r2 = client.post("/api/payments/retry", json={"payment_id": "p1"},
                      headers={"Idempotency-Key": "k1"})
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json == r1.json
    # (no assertion on charge_gateway.retry call count)
```

## Verify evidence (as attached to the PR)

```
verify loop @ 8f2c1a9 — 2026-06-18T14:02:11Z
  ✓ typecheck  ok
  ✓ lint       ok
  ✓ test       .venv/bin/python -m pytest -q tests/ --cov=app --cov-fail-under=80
               19 passed, coverage 91%
verify: ALL GREEN
```

No failures logged. No `UNVERIFIED` items declared.

## Other facts available to the reviewer

- `charge_gateway.retry()` (`app/paysvc/gateway.py:112`) calls the external
  payment processor — **not idempotent on the gateway side**; a second call
  with the same `payment_id` before the first commits will process a second
  real charge.
- Load pattern in production: retries are triggered by an automatic client
  retry-on-timeout policy, which can and does fire two requests with the same
  `Idempotency-Key` within milliseconds of each other under gateway latency
  spikes — this is the exact condition the check-then-act gap at
  `retry.py:47-54` would miss, despite the unique index existing in the schema.
- The PR description states: "Area of least confidence: none — straightforward
  CRUD-shaped feature."
- One reviewer (`t.owens`) is named in the PR as having approved. No second
  reviewer is listed.
