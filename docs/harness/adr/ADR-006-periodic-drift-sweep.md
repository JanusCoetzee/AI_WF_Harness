# ADR-006 — Wider-than-one-change drift sweep joins retro, not a new cadence

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-25 |
| Deciders | janus (Driver) |
| REQs served | N/A — harness process improvement, not tied to a work-item REQ/CHG |

## Context

A comparison against `github/spec-kit` surfaced its `/speckit.converge` step:
a periodic check that re-assesses the whole codebase against specs, catching
drift that accumulates across many small changes rather than within any one
of them.

This harness's brownfield recon (B1) is deliberately scoped to the change
under work — "no estate-wide archaeology" — which is correct for keeping any
single `CHG-###` change cheap, but it also means nothing ever asks whether
drift has accumulated *across* many small, individually-correct changes. `
/harness-retro` already exists on a fortnightly/post-release cadence to audit
the harness's own performance (`stages/08-operate-learn.md`). If we don't
decide anything here, that class of drift has no detector at all.

## Options considered

### Option A — New periodic gate, independent of `/harness-retro`

- Sketch: a scheduled `MAINT`-style dossier, but scoped to "does recent
  CHG-### history still match what RECON.md files claimed at the time," run
  monthly regardless of retro cadence.
- Pros: guaranteed cadence independent of whether a retro happens to cover it.
- Cons: another recurring ceremony item competing for calendar time; retro
  already exists as the reflection checkpoint — a second one invites the
  "which meeting does this belong in" confusion.
- Risks: redundant with retro; likely to be the first thing skipped under
  time pressure, becoming a paper gate.

### Option B — Add it as a required retro checklist item, no new cadence

- Sketch: `harness-retro` gains one required check: "sample N recent CHG-###
  changes; confirm their RECON.md claims still hold against current code
  (spot drift accumulated across many small changes that no single recon
  would catch)." Reuses the existing "fortnightly or after release" retro
  cadence from `stages/08-operate-learn.md`.
- Pros: zero new ceremony surface; retro already exists specifically to audit
  the harness's own performance; this is a natural extension of that mandate.
- Cons: cadence is whatever retro's cadence is (fortnightly/post-release), not
  a guaranteed fixed interval — acceptable given this is a drift *detector*,
  not a safety-critical control.
- Risks: none beyond retro itself being skipped, which is an existing risk
  this ADR doesn't change.

## Decision

**Option B.** Add as a required `harness-retro` checklist item, reusing
existing cadence rather than inventing a new one.

AI recommendation: Option B — the drift this check catches is a slow
accumulation, not an urgent per-change risk, so tying it to retro's existing
reflective cadence fits its actual time-scale better than a guaranteed but
easily-skipped monthly gate would.

## Consequences

**Easier:** drift across many small brownfield changes gets a recurring check
instead of none, at zero new process overhead.

**Harder / new commitments:** `harness-retro` grows one more required item;
if retro itself is skipped or rushed, this detector is skipped along with it
— an existing risk this decision inherits rather than introduces.

**Tripwire to revisit this ADR:** if retro's actual cadence proves too
infrequent to catch drift before it compounds into a real incident, reconsider
Option A — a dedicated, guaranteed-cadence sweep independent of whether retro
happens on schedule.
