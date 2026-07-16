# IDEA — PayGuard exception triage

| Field | Value |
| --- | --- |
| Status | Approved (G0) — drill |
| Driver | janus |
| Sponsor (T1 only) | Head of Payment Operations |
| Date | 2026-07-17 |

## Problem statement

14 analysts hand-triage ~1,100 payment exceptions/day at ~6 min each; ~30% of cases
bounce to a second team because first routing was wrong. SLA breaches rise ~8% q/q.
Cost: ~110 analyst-hours/day, rising breach penalties, attrition (2 resignations).

## Why now

Breach trend crosses the ops-risk appetite line within two quarters; sanctions-hold
timelines make misrouting a compliance exposure, not just an efficiency drag.

## Smallest testable version

Classify one exception type (format failures) from hub events and recommend a queue
in shadow mode; measure recommendation accuracy against what analysts actually did.

## Kill criteria

- Shadow-mode routing accuracy < 75% after 4 weeks of tuning → kill.
- Approved LLM gateway cannot meet 2s p95 at peak → kill (rules-only fallback ships instead).
- Redaction of remittance text proves infeasible to the DPO's standard by end of M2 → kill.

## Do-nothing steelman

Hiring 2 analysts costs less than a squad-quarter and carries zero model risk; the
case tool vendor promises routing rules "next year". Honest answer: vendor timelines
have slipped twice, and hiring doesn't fix the 30% bounce rate — but if the bounce
rate were the only problem, better queue definitions alone might halve it. Discovery
must check that cheaper fix first (REQ open question).

## Risk tier proposal

| Question | Answer |
| --- | --- |
| Moves money or affects customer outcomes? | Indirectly — routing delays affect payment outcomes; sanctions holds have compliance timelines |
| Touches data above Internal? | Yes — payment data incl. remittance PII, Confidential |
| Regulatory / reporting surface? | Yes — sanctions-hold handling timelines |
| Blast radius if wrong? | Misrouted sanctions hold; systematic misclassification at 1,100/day scale |
| **Proposed tier + rationale** | **T1** — Confidential data + compliance timelines + LLM influencing operational decisions |
