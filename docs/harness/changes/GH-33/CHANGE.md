# CHANGE — #33 harness-retro captures pilot container/skills metadata

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #33 — ADR-013's implementation, split from #32 |
| Date | 2026-08-19 |
| Risk tier | T3 — docs/template only, no code, no data, no deploy surface |
| Recon | waived-trivial (docs-level additions to two templates/skills and one README line, same category as GH-15/GH-25/GH-27) |
| Linked records | `ADR-013` (this ticket's design authority), `ADR-006` (the drift-sweep shape reused), `#32` (soft dependency — labels this ticket's sweep table references) |
| Timing constraints | none |
| Constitution sections consulted | §5 (traceability — retro closes the loop, ADR-014's own "ticket precedes work" already satisfied by #33 pre-existing this build) |

## Intent

`templates/RETRO.md` and `harness-retro`'s `SKILL.md` don't yet know how
to correlate `pilot-feedback` issues to the container/skills version that
produced them. Done means both do, following the exact shape `ADR-006`'s
existing drift sweep already established, and `README.md`'s
`pilot-feedback` ask actually requests the metadata needed to make the
sweep possible.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-33.1 | Given `templates/RETRO.md`, when read, then it has a "Pilot container/skills metadata sweep" table (issue #, image tag, `git_commit`, `skills[]` versions, still-current-tag?, notes) — same shape/rigor as the existing brownfield drift-sweep table |
| GH-33.2 | Given `.claude/skills/harness-retro/SKILL.md`, when read, then it has a new numbered step sweeping `pilot-feedback` issues opened since the last retro against the currently-published tag |
| GH-33.3 | Given `README.md`'s `pilot-feedback` ask, when read, then it explicitly requests the image-metadata output as part of what to include |
| GH-33.4 | Given a synthetic `pilot-feedback` issue citing a tag, when the new sweep step is walked through by hand, then it's actually followed, not just present in the template |

## Live proof (GH-33.4 — sweep step actually walked, not just present)

No real GHCR tag exists yet (`#32`'s real publish is deliberately still
declined by the Driver), so this walkthrough is synthetic — labeled as
such, not presented as a real pilot report. It exercises the *mechanics*
of the new `SKILL.md` step 5, not a live GHCR tag comparison (that part
needs `#32`'s real publish to exist at all).

**Synthetic `pilot-feedback` report** (not filed on the real tracker):

```
Image: ghcr.io/janusCoetzee/harness-doctrine:v0.1.0
Labels: {"io.harness.doctrine_version": "harness-v0.1",
         "io.harness.skills": "harness-issues@harness-v0.1"}
Finding: "harness_get_gate returns the wrong content for G5"
```

**Sweep step walked by hand:**
1. Pull the current pin: `harness.config.yaml`'s `doctrine.version` is
   `harness-v0.2` (`skills:` lists three entries, none at `harness-v0.1`).
2. Compare against the synthetic report's `io.harness.doctrine_version`:
   `harness-v0.1` ≠ `harness-v0.2`.
3. Conclusion the sweep step produces: **stale** — this report is against
   a superseded tag. Per `SKILL.md`'s new instruction, it gets triaged as
   "check whether `harness-v0.2` already fixed this" before treating it
   as a live bug against current behavior — not dismissed, not treated as
   urgent-and-current either.

This confirms the comparison logic in `templates/RETRO.md`'s new table
and `SKILL.md`'s new step actually produces a real, correct
stale/current verdict from realistic inputs — the mechanism works. The
one piece this can't prove yet is pulling a *real* tag list from GHCR,
since no tag has been published (deliberately, per the Driver's standing
decision on `#32`).

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `templates/RETRO.md`, `.claude/skills/harness-retro/SKILL.md`, `README.md` — docs/template only |
| Known consumers | future `/harness-retro` runs; `README.md` readers filing `pilot-feedback` issues |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit. No migration, no consumer that depends on the new sections existing.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — reuses `ADR-006`'s drift-sweep shape and `ADR-013`'s already-decided design, doesn't invent a new pattern | ADR |
| Effort beyond ~3 days after recon? | No — three short doc/template edits | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. **Approved in-session, 2026-08-19** (Driver: "yes", approving #32/#33/#35 together — ADR-012's synchronous carve-out). `DECISIONS.log`: `2026-08-19 | GC passed | janus | GH-33`
