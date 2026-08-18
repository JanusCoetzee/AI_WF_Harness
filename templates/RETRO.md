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

## Brownfield drift sweep (ADR-006)

Sample N recent `CHG-###` changes; confirm their `RECON.md` claims still hold
against current code. This catches drift accumulated across many small,
individually-correct changes that no single recon would have caught.

| CHG-### | RECON.md claim checked | Still holds? | Notes |
| --- | --- | --- | --- |

## Pilot container/skills metadata sweep (ADR-013, GH-33)

For each `pilot-feedback`-labeled issue opened since the last retro: which
image tag and `skills[]` composition produced it, and is that still the
current published tag? Same purpose as the brownfield drift sweep above —
catching drift, here between what a pilot participant actually ran and
what's current — applied to container versions instead of `RECON.md`
claims. Pull the reported tag/labels from the issue itself (`README.md`
asks filers to include `docker inspect --format='{{json .Config.Labels}}'
<image>` output, or the running container's own `/api/health`/manifest
`git_commit`/`skills[]` fields); compare against the latest tag actually
published to GHCR.

| Issue # | Image tag | git_commit (short) | skills[] versions | Still current tag? | Notes |
| --- | --- | --- | --- | --- | --- |

## Ceremony audit

Which harness ceremony produced no value this cycle? Propose the cut. (A harness that
only grows becomes the bureaucracy it replaced.)

## Actions

Owners and dates, tracked to closure — an untracked action is an audit finding.

| # | Action | Owner | Due | Done |
| --- | --- | --- | --- | --- |

## Feed-forward

What goes into the next cycle's Stage 00 (IDEA.md candidates, harness changes):
