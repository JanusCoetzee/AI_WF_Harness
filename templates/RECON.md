# RECON — CHG-###

Understanding before changing. Every claim about existing behavior cites `file:line`
or a test — no claims from memory.

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| Entry point(s) of the touched behavior | | |
| Call path (in order) | | |
| State touched (tables, caches, queues, files) | | |
| Config / flags that alter this path | | |

## Consumers found

Include the out-of-repo kind — cron jobs, other services, reports, spreadsheets
someone exports. These are the ones that bite.

| Consumer | How it depends on touched behavior | Found via |
| --- | --- | --- |

## Implicit contracts (Hyrum's law inventory)

Undocumented behaviors someone may rely on: ordering, rounding mode, error shapes,
timezone handling, nulls-vs-empties, timing, retry semantics.

| Observed behavior | Evidence (file:line / test) | Safe to change? |
| --- | --- | --- |

## Test coverage reality

- Existing tests covering the touched path: <paths, or "none">
- **Characterization tests added** (pin current behavior BEFORE changing it): <paths>
- Behaviors deliberately left unpinned + why:

## Surprises / archaeology

Significant undocumented decisions discovered in the touched code. Each becomes a
retroactive ADR describing the status quo — only for what we touch, no estate-wide dig.

| Finding | Action (retro-ADR-### / accepted as-is) |
| --- | --- |

## Revised blast radius & tier

Corrections to CHANGE.md's estimate. If tier or effort grew: escalation triggers in
CHANGE.md get re-answered — honestly.

## Go / No-go

- [ ] Blast radius confirmed, no "unknown" rows above
- [ ] Characterization tests green against unchanged code
- [ ] Escalation triggers re-checked after what recon revealed
- **Recommendation:** go / no-go / escalate — <one sentence why>
