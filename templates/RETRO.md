# Retro — <cycle / release>

| Field | Value |
| --- | --- |
| Date | |
| Participants | |
| Scope (release/period) | |

## Outcomes vs. intent

- What shipped vs. what the PRD promised (walk the REQ list):
- Success measures: where do the numbers stand against the PRD's goals?

## Gate performance

| Gate | What it caught | What slipped through it | Adjustment proposed |
| --- | --- | --- | --- |

## AI-pairing performance

Where the LLM partnership shone and where it burned time. Be specific — these feed
directly into `CLAUDE.md` rule changes.

| Pattern observed | Shine / Burn | Rule or practice change |
| --- | --- | --- |
| e.g. thrash loop on flaky integration test | Burn | Added "stop after 2 identical failures" rule |
| e.g. adversarial self-review caught rounding bug pre-G5 | Shine | Keep; add rounding cases to eval dataset |

## Ceremony audit

Which harness ceremony produced no value this cycle? Propose the cut. (A harness that
only grows becomes the bureaucracy it replaced.)

## Actions

Owners and dates, tracked to closure — an untracked action is an audit finding.

| # | Action | Owner | Due | Done |
| --- | --- | --- | --- | --- |

## Feed-forward

What goes into the next cycle's Stage 00 (IDEA.md candidates, harness changes):
