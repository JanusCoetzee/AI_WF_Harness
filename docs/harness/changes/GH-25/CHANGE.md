# CHANGE — GH-25 README Quickstart omits gates/, stages/, templates/, docs/

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #25 — surfaced answering a real adoption question, 2026-08-17 |
| Date | 2026-08-17 |
| Risk tier | T3 — documentation only, no code path, no data, no deploy surface |
| Recon | waived-trivial (docs-level: README additions describing files that already exist and are already load-bearing — same category as GH-15) |
| Linked records | GH-15 (2026-08-12) fixed an adjacent, narrower instance of this same class of gap — added `OPERATING-PROTOCOL.md` + 3 scripts to Quickstart step 1 without auditing whether the rest of the list was ever complete. It wasn't. |
| Timing constraints | none |
| Constitution sections consulted | §8 (retroactive documentation only for what's touched — this closes exactly the gap found, no wider archaeology) |

## Intent

Quickstart step 1 lists five things to copy into an adopting repo but omits
`gates/`, `stages/`, `templates/`, and the `docs/` trio — despite every
skill's own header citing `stages/`/`templates/` by relative path as its
authoritative source. Following today's Quickstart literally into a fresh
repo breaks every skill immediately. Done means step 1 lists everything a
fresh repo actually needs today, with a note on why (ADR-002's target
end state serves this centrally; that service isn't live yet).

## Acceptance criteria

| # | Given / When | Then |
| --- | --- | --- |
| GH-25.1 | Quickstart step 1 | lists `gates/`, `stages/`, `templates/`, and `docs/` (`PHILOSOPHY.md`, `OPERATING-MODEL.md`, `STANDARDS.md`) alongside the existing five items |
| GH-25.2 | Quickstart step 1 | explains why (today's vendor-everything fallback vs. ADR-002's centrally-served target state, not yet live) |
| GH-25.3 | Directory map (already correct) | left unchanged — it already lists these directories, only the copy instructions were incomplete |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | README.md only |
| Known consumers | humans reading README when adopting the harness into a new repo |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — describes files already present, no new convention | ADR |
| Effort beyond ~3 days after recon? | No — minutes | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. `DECISIONS.log`: `2026-08-17 | GC passed | janus | GH-25`
