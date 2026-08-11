# Scenario: paysvc — fortnightly retro (Stage 08 / G8)

*Input handed to the harness: one cycle's worth of history — past changes, their
original recon claims, incidents, and gate notes. The runner produces only
`RETRO.md` from `/harness-retro`, strictly from harness skill instructions and
the brownfield drift-sweep checklist item (ADR-006). Fictional but
representative. Cycle window: 2026-06-01 (last retro) through 2026-06-29.*

## Changes shipped this cycle

| CHG | Date | What | Gate notes |
| --- | --- | --- | --- |
| CHG-101 | 2026-05-02 (prior cycle, recon claim carried forward) | Added `/api/payments/status` read endpoint | G4 clean |
| CHG-104 | 2026-06-04 | Settlement batch job tuning | G4 clean |
| CHG-107 | 2026-06-11 | Notification retry logic | **Shipped without a verify log attached; caught at G4 gate-check, which blocked the gate until `scripts/verify.sh --log` was run retroactively** |
| CHG-108 | 2026-06-16 | Added bearer-token auth support alongside existing session-cookie auth, for the new partner API | G4 clean; G5 self-review flagged a missing audit-log entry for token-auth failures *before* human review — fix landed same commit |
| CHG-109 | 2026-06-19 | Fixed duplicate settlement-notification emails (root cause: notifier retried on timeout with no dedupe) — closes incident INC-2026-014 | G4 clean |
| CHG-110 | 2026-06-25 | Export job: added a CSV column for partner ID | G4 clean |
| CHG-114 | 2026-06-18 | Idempotent payment retry (see `review-g5.md` if scored separately) | G5 review record on file |

## Original recon claims to re-check (sample for the drift sweep)

Pulled verbatim from each change's `RECON.md` at the time it was written:

- **CHG-101's `RECON.md`** (2026-05-02): *"Authentication for all `/api/payments/*`
  routes uses session cookies exclusively (`auth/middleware.py:44`); no bearer-token
  path exists in this service."*
  **Current state (as of this retro):** CHG-108 (2026-06-16) added a bearer-token
  auth path to the same file, `auth/middleware.py:44-79`, specifically to support
  the new partner API. CHG-101's claim ("cookies exclusively... no bearer-token
  path exists") **no longer holds** — nothing re-opened or corrected CHG-101's
  RECON.md when CHG-108 landed.

- **CHG-104's `RECON.md`** (2026-06-04): *"The settlement batch job
  (`jobs/settle.py:12`) runs single-threaded via a cron trigger; no concurrency
  control is needed because only one instance is ever scheduled."*
  **Current state:** unchanged — still single-threaded, still one cron schedule.
  Claim **still holds**.

- **CHG-110's `RECON.md`** (2026-06-25): *"The export job (`export/writer.py:80`)
  writes CSV only; no other output format is consumed downstream."*
  **Current state:** unchanged — still CSV-only. Claim **still holds**.

## Incidents this cycle

- **INC-2026-014** (2026-06-17): duplicate settlement-notification emails sent to
  ~1,400 customers. Root cause: the notifier's retry-on-timeout logic had no
  dedupe key, so a slow SMTP response triggered a second send. Fixed by CHG-109.
  Blameless post-incident review held 2026-06-20; the one action item
  ("add a dedupe key to all outbound notification retries, not just settlement")
  is recorded with owner `m.olsen`, due 2026-07-10, **not yet done** as of this
  retro.

## AI-pairing notes from the cycle

- **Burn:** CHG-107's session spent roughly 40 minutes re-running a flaky
  integration test (`test_settlement_batch_timing`) before identifying it
  depended on wall-clock time rather than a frozen clock; fixed by pinning
  `freezegun.freeze_time()` in the test fixture.
- **Shine:** CHG-108's adversarial self-review (`/harness-review` step 1) caught
  the missing audit-log entry for failed token-auth attempts *before* human
  review reached it — human reviewer's diff comment: "good catch, would have
  missed this."

## Ceremony note

Three of the seven changes this cycle (CHG-104, CHG-110, and the carried-forward
CHG-101) were single-file, sub-50-line changes on components with existing
90%+ test coverage and no tier escalation — each still went through a full
`CHANGE.md` + `RECON.md` + GC pass.

## Outstanding action from the last retro (2026-06-01)

`RETRO-2026-06-01.md` recorded one action: *"Add a contract test for the
downstream tax-reporting feed's dependency on `paysvc`'s interest-figure
rounding."* Owner: `m.olsen`. Due: 2026-06-20. **Status: not done, not
mentioned again since.**
