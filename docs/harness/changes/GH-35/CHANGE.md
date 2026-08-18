# CHANGE — #35 templates/ISSUE.md gets a lightweight collapse for tickets filed mid-build

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Source (ticket / requester — named) | GitHub issue #35 — first self-application of `ADR-014` |
| Date | 2026-08-19 |
| Risk tier | T3 — docs/template only, no code, no data, no deploy surface |
| Recon | waived-trivial (docs-level addition to a template's own instructions, same category as GH-15/GH-25/GH-27) |
| Linked records | `ADR-014` (this ticket's design authority), `ADR-010` (the reused one-file/case-conditional pattern), `#34` (the concrete comparison case) |
| Timing constraints | none |
| Constitution sections consulted | §5 (traceability — `ADR-014` itself, applied to the ticket that implements it) |

## Intent

`templates/ISSUE.md` only had one shape — full Context, vertical-slice
table, formal acceptance criteria, Proof, DoR — disproportionate ceremony
for a fast, mid-build finding `ADR-014` now requires a ticket for. Done
means the template has an inline, self-explanatory collapse for exactly
that case, reusing `ADR-010`'s already-decided pattern (one file,
case-conditional, not a second file) rather than inventing a new shape.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-35.1 | Given `templates/ISSUE.md`, when read directly (not through the skill), then the mid-build collapse is self-explanatory — states what it is, when to use it, and what it skips, without requiring `ADR-010`/`ADR-014` to be read first |
| GH-35.2 | Given `#34` (filed after its own fix — the wrong-order case `ADR-014` names), when rewritten using the new collapsed format, then it's genuinely faster to fill without losing what made it useful as a record |
| GH-35.3 | Given a real planned-work ticket (`#32`'s or `#33`'s own bodies), when compared against the unchanged full template, then nothing about the full-shape path changed — the collapse is additive |
| GH-35.4 | Given `.claude/skills/harness-issues/SKILL.md`, when it references ticket-writing, then it points at the same collapse instruction, not a duplicate or contradiction |

## Live proof

**GH-35.1** — the collapse block sits right after the "ticket is the
prompt" line in `templates/ISSUE.md`, states the three questions inline
(what's broken / why significant / what fixed looks like), and names
exactly which sections it skips (Vertical slice, Acceptance criteria,
Proof) with inline `*(Skip for a mid-build finding ticket...)*` markers
at each of those sections themselves — findable by reading the template
top to bottom, no external reference required.

**GH-35.2** — `#34` rewritten using the new shortcut, for comparison
(not applied to the real issue — a comparison exercise per AC's own
wording):

> **What's broken:** `app/doctrine.py::_git_commit()`'s `git rev-parse`
> call fails with "detected dubious ownership" when `/harness` is owned
> by a different uid than the process running git.
>
> **Why it's significant:** platform-level — the fix (`git config
> --system --add safe.directory`) is a container-wide config change
> affecting how *every* process resolves git provenance, in both content
> modes, and the underlying risk was already latent in `#31`'s
> already-shipped, already-closed container (bind-mount ownership just
> happened not to trip it there).
>
> **What fixed looks like:** `git rev-parse` succeeds regardless of
> `/harness`'s ownership, verified live for baked mode; mount mode was
> never observed to actually fail (latent risk, not a reproduced
> incident), so no historical impact to remediate — forward-only
> hardening.

Three short paragraphs vs. the original's four full prose sections
("What happened" / "The defect" / "Disposition" / "Why this has its own
issue"). Same substance, genuinely faster to write — confirms the
shortcut isn't losing what made `#34` useful as a record, it's cutting
the scaffolding around it.

**GH-35.3** — `#32`'s and `#33`'s own ticket bodies (both filed before
this change) are unaffected; nothing in the full-shape sections was
touched, only additive skip-markers and the new collapse block were
added.

**GH-35.4** — `.claude/skills/harness-issues/SKILL.md` gained a "Mode
C — mid-build finding (ADR-014)" section pointing at the template's own
instruction rather than restating or diverging from it.

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Modules / services touched | `templates/ISSUE.md`, `.claude/skills/harness-issues/SKILL.md` — docs/template only |
| Known consumers | future ticket authors (human or LLM) using either file |
| Data elements | none |
| Deploy surface | none |

## Rollback note

Revert the commit. No migration, no consumer that depends on the new sections existing.

## Escalation triggers — answer all four honestly

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface, data flow, or LLM touchpoint? | No | G2 |
| Decision that deviates from the existing pattern? | No — reuses `ADR-010`'s already-decided one-file/case-conditional pattern, doesn't invent a new one | ADR |
| Effort beyond ~3 days after recon? | No — two short template/skill edits | G1 |
| Tier raised during recon? | No | re-approve |

## GC sign-off

T3: Driver. **Approved in-session, 2026-08-19** (Driver: "yes", approving #32/#33/#35 together — ADR-012's synchronous carve-out). `DECISIONS.log`: `2026-08-19 | GC passed | janus | GH-35`
