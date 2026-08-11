# IDEA — PayGuard: automated payment-exception triage & routing

| Field | Value |
| --- | --- |
| Status | Draft |
| Driver | AI pair (blind-run production, evals/harness) |
| Sponsor (T1 only) | Head of Payment Operations |
| Date | 2026-08-12 |
| Constitution sections consulted | §6 data handling (remittance free-text carries PII/account numbers — Confidential, prompt-ceiling relevant), §4 milestones (walking-skeleton framing below) |

## Problem statement

14 payment-operations analysts manually triage ~1,100 exceptions/day (format
failures, sanctions near-miss holds, insufficient-funds returns, suspected
duplicates, cutoff misses) at ~6 minutes average handle time. ~30% of routed
cases bounce to the wrong specialist team and get re-routed, burning analyst
time twice. SLA breaches are up ~8% QoQ and two analysts have resigned citing
workload. Cost today: SLA breach exposure (including sanctions-timeline
exposure, which carries compliance consequences), attrition, and the
opportunity cost of skilled analysts spending time on routing instead of
judgment calls.

## Why now

SLA breach trend is accelerating (+8% QoQ) and headcount is already leaking
(two resignations cited as workload-driven) — the queue is degrading faster
than it can be staffed against, and the misrouting tax (30% bounce rate) means
headcount growth alone wouldn't fix the underlying problem.

## Smallest testable version

Classify incoming exceptions into the correct specialist queue (routing only,
no auto-resolution) for the two highest-volume, lowest-compliance-risk
exception types (format failures, cutoff misses), with an analyst confirming
every routing decision before the case leaves the queue. Tests whether
classification accuracy meaningfully cuts the 30% bounce rate before any
sanctions-adjacent case type is in scope.

## Kill criteria

- If a 4-week shadow run (model suggests, analyst still routes manually, no
  behavior change) shows routing-suggestion accuracy below 75% on the two
  in-scope exception types, kill before any live routing.
- If discovery shows the true bounce-cost is materially smaller than the
  presenting 30% figure (e.g. re-routing is fast and cheap in the current
  case tool), the ROI case likely doesn't clear one squad/one quarter — kill.
- If the approved internal LLM gateway cannot meet the EU data-residency
  constraint for this workload, kill or re-scope before build.

## Do-nothing steelman

Headcount could be added instead: 14 → ~18-20 analysts might absorb the
current SLA-breach trend without any AI build, avoiding new model-risk,
explainability, and audit-trail obligations entirely. Given attrition is
already running ahead of hiring and the *routing* step (not raw triage
judgment) is the specific bottleneck (30% bounce), pure headcount doesn't fix
the root cause — but it is cheaper and faster to start than a squad-quarter
build, and it's the honest baseline this idea has to beat.

## Risk tier proposal

| Question | Answer |
| --- | --- |
| Moves money or affects customer outcomes? | Not directly (routing only, no auto-resolution of payments) — but sanctions-hold exceptions carry regulatory timelines, and misrouting one has compliance consequences |
| Touches data above Internal? | Yes — remittance free-text routinely contains customer names, account numbers, invoice details; payment data is classified Confidential |
| Regulatory / reporting surface? | Yes — sanctions-hold handling is regulatory-timeline-bound; automated routing decisions need an audit trail an examiner could reconstruct |
| Blast radius if wrong? | Misrouted sanctions-hold case → missed regulatory timeline (compliance exposure); misrouted ordinary exception → re-bounce, no worse than current-state failure mode |
| **Proposed tier + rationale** | T1 — Confidential data in scope, regulatory (sanctions-timeline) surface, and the specific failure mode (misrouted sanctions hold) has direct compliance consequences even though the system doesn't move money itself. The smallest-testable-version above deliberately excludes sanctions-hold cases from the first shadow run precisely because of this tier. |
