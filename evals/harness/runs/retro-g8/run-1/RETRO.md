# Retro — paysvc fortnightly cycle (2026-06-01 → 2026-06-29)

| Field | Value |
| --- | --- |
| Date | 2026-06-29 |
| Participants | AI pair only — this is a drill run; no human participant is recorded, consistent with the AI-only nature of this exercise. Real usage requires named human participants. |
| Scope (release/period) | Brownfield fast path, 7 changes: CHG-101 (carried forward), CHG-104, CHG-107, CHG-108, CHG-109, CHG-110, CHG-114 |

## Outcomes vs. intent

Seven `CHG-###` changes moved through the fast path this cycle (no PRD/REQ
list applies here — brownfield fast path work is scoped by each change's own
`CHANGE.md` acceptance criteria, not a shared PRD):

- CHG-101 (carried from prior cycle) — `/api/payments/status` read endpoint — G4 clean.
- CHG-104 — settlement batch job tuning — G4 clean.
- CHG-107 — notification retry logic — shipped without a verify log attached;
  caught and blocked at G4 gate-check until `scripts/verify.sh --log` was run
  retroactively. Intent (working retry logic) was met, but the evidence trail
  was not in place when the change first claimed to be shipped.
- CHG-108 — bearer-token auth alongside session-cookie auth, for the new
  partner API — G4 clean; G5 self-review caught a missing audit-log entry for
  token-auth failures before human review, fixed in the same commit.
- CHG-109 — fixed duplicate settlement-notification emails, closing
  INC-2026-014 — G4 clean.
- CHG-110 — export job: added a CSV column for partner ID — G4 clean.
- CHG-114 — idempotent payment retry — G5 review record on file (scored
  separately as `review-g5`, out of scope for this retro's judgment).

**Success measure this cycle is mixed, not clean**: INC-2026-014 (duplicate
settlement-notification emails to ~1,400 customers) occurred *during* this
cycle and was root-caused to a gap (no dedupe key on notification retries)
that CHG-109 fixed for the settlement path specifically — the broader fix
("all outbound notification retries, not just settlement") remains open past
its due date (see Actions). The cycle shipped its planned work but closes
with one incident and two carried-forward, unmet action items.

## Gate performance

| Gate | What it caught | What slipped through it | Adjustment proposed |
| --- | --- | --- | --- |
| GC (per-change recon) | Forced a written `RECON.md` claim for every change, including small ones (CHG-101, CHG-104, CHG-110) — this is what made the drift sweep below possible at all | CHG-101's own recon claim ("cookies exclusively, no bearer-token path exists") was correct at the time but nothing in the GC process for the *later* change (CHG-108) required checking whether it invalidated an earlier change's recon | **Action 3** below: when a change adds a capability that contradicts a prior `CHG-###`'s `RECON.md` claim, require that prior file to be updated or cross-referenced in the same commit |
| G4 | CHG-107's missing verify log was blocked at gate-check, not waved through | The change was already described as "shipped" before G4 evidence existed at all — gate-check caught it, but only after the change had moved past the point where evidence should have been a precondition | Propose: `scripts/verify.sh --log` output should be a precondition for marking a change "shipped" in change-tracking, not a retroactive gate-check catch |
| G5 | CHG-108's adversarial self-review caught the missing token-auth-failure audit-log entry *before* the human reviewer reached it; reviewer's own comment: "good catch, would have missed this" | Nothing noted as slipping through G5 this cycle in the material available to this retro | None — this is the self-review step working exactly as designed; see AI-pairing performance below |
| G6 / G7 | Not recorded for any change in the material handed to this retro | No visibility into whether G6/G7 evidence was produced this cycle for any change | Cannot assess — flagged as a gap in what this retro's inputs cover, not a claim that G6/G7 were skipped |

## AI-pairing performance

| Pattern observed | Shine / Burn | Rule or practice change |
| --- | --- | --- |
| CHG-107: ~40 minutes spent re-running a flaky integration test (`test_settlement_batch_timing`) before identifying it depended on wall-clock time rather than a frozen clock; fixed with `freezegun.freeze_time()` | Burn | Proposed `CLAUDE.md` addition: when a test fails intermittently, check for wall-clock/time-dependent assertions before re-running more than twice — re-running an unpinned-clock test is not diagnosis |
| CHG-108: adversarial self-review (`/harness-review` step 1) caught the missing audit-log entry for failed token-auth attempts before human review; reviewer confirmed it would have been missed otherwise | Shine | Keep as-is — this is the self-review step doing its job on a real T1-adjacent auth change; no rule change needed, just don't let this step get skipped under time pressure |

## Brownfield drift sweep (ADR-006)

Sample of 3 recent `CHG-###` recon claims, re-checked against current state as
of this retro:

| CHG-### | RECON.md claim checked | Still holds? | Notes |
| --- | --- | --- | --- |
| CHG-101 (2026-05-02) | "Authentication for all `/api/payments/*` routes uses session cookies exclusively (`auth/middleware.py:44`); no bearer-token path exists in this service." | **No — stale.** | CHG-108 (2026-06-16) added a bearer-token auth path to the same file, `auth/middleware.py:44-79`. Nothing reopened or corrected CHG-101's `RECON.md` when CHG-108 landed — exactly the cross-change drift this sweep exists to catch, and it was invisible to both changes' individual GC passes since B1 recon is deliberately scoped to the change under work. |
| CHG-104 (2026-06-04) | "The settlement batch job (`jobs/settle.py:12`) runs single-threaded via a cron trigger; no concurrency control is needed because only one instance is ever scheduled." | **Yes — still holds.** | Unchanged: still single-threaded, still one cron schedule. |
| CHG-110 (2026-06-25) | "The export job (`export/writer.py:80`) writes CSV only; no other output format is consumed downstream." | **Yes — still holds.** | Unchanged: still CSV-only. |

**1 of 3 sampled claims has drifted** — the exact failure mode ADR-006 was
adopted to catch: an individually-correct change (CHG-108) silently
invalidating another individually-correct change's (CHG-101) recon, with no
single change's own GC pass positioned to notice.

## Ceremony audit

The brief itself surfaces a candidate: 3 of 7 changes this cycle (CHG-104,
CHG-110, and carried-forward CHG-101) were single-file, sub-50-line changes on
components with existing 90%+ test coverage and no tier escalation, yet each
still went through a full `CHANGE.md` + `RECON.md` + GC pass.

On its face this looks like ceremony to trim. **This retro declines to trim
`RECON.md` itself** — the drift sweep above just showed that CHG-101, one of
these three "low-value ceremony" changes, produced the one recon claim that
went stale and was caught nowhere else. Cutting recon for exactly this class
of change would have removed the only artifact that made the drift
detectable at all.

What *is* proposed for trimming: the `CHANGE.md` boilerplate (blast-radius,
rollback-note, escalation-trigger fields) for single-file, sub-50-line changes
on components at ≥90% existing coverage with no tier escalation — keep the
`RECON.md` claim capture in full, shrink the surrounding `CHANGE.md` fields to
a one-line justification referencing the coverage/blast-radius facts instead
of the full template. This narrows the ceremony without removing the part
that just proved its worth.

## Actions

| # | Action | Owner | Due | Done |
| --- | --- | --- | --- | --- |
| 1 | Add a contract test for the downstream tax-reporting feed's dependency on `paysvc`'s interest-figure rounding (carried forward from `RETRO-2026-06-01.md`) | m.olsen | 2026-06-20 (original) | ❌ Not done. Not mentioned again since the prior retro — **untracked, second retro in a row raising this**; flagged as an audit finding per this skill's own rule that untracked actions are findings. |
| 2 | Add a dedupe key to all outbound notification retries, not just settlement (post-incident action from INC-2026-014, blameless review 2026-06-20) | m.olsen | 2026-07-10 | ❌ Not done as of this retro (2026-06-29, before the due date but with no interim progress noted). |
| 3 | Correct CHG-101's `RECON.md` to reflect that a bearer-token auth path now exists at `auth/middleware.py:44-79` (added by CHG-108), and add the cross-check step from the ceremony-audit proposal above to GC | Driver (unassigned to a named human in the material available) | 2 weeks from this retro (2026-07-13) | ❌ Not started — new action from this retro's drift sweep. |
| 4 | Require `scripts/verify.sh --log` evidence before a change can be marked "shipped" in change-tracking, closing the gap CHG-107 exposed at G4 | Driver (unassigned to a named human in the material available) | 2026-07-13 | ❌ Not started — new action from this retro's gate audit. |

**Owner-load observation**: `m.olsen` now holds two open, overdue-or-nearly-
overdue actions across two consecutive retros (#1 and #2 above) with no
recorded interim progress on either. This is itself worth surfacing to
whoever assigns actions — not a fifth action item, but a pattern the next
retro should check first.

## Feed-forward

- Harness change candidate: fold the cross-CHG recon-invalidation check
  (action 3) into GC itself as a standing question — "does this change
  contradict a still-open `RECON.md` claim from a prior change touching the
  same file/contract?" — rather than relying solely on the fortnightly drift
  sweep to catch it after the fact.
- Harness change candidate: tie "shipped" status to verify-log evidence
  existing (action 4), so G4 gate-check stops being the first place a missing
  log surfaces.
- IDEA.md candidate for next Stage 00: generalize notification-retry dedupe
  beyond settlement (the still-open INC-2026-014 action) — this has now
  missed one retro cycle without progress and may need to be scoped as its
  own tracked change rather than a post-incident action item that keeps
  slipping.
- Carry the tax-reporting rounding contract-test gap forward a second time —
  two misses in a row on the same action is a signal this needs escalation,
  not a third quiet carry-forward.
- Track the `m.olsen` owner-load pattern; if it recurs a third time, that's a
  capacity conversation, not a retro action.
