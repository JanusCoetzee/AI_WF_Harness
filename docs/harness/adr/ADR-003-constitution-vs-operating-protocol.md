# ADR-003 — CLAUDE.md is the constitution; procedure splits into a separate operating-protocol doc

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-25 |
| Deciders | janus (Driver) |
| REQs served | N/A — harness process improvement, not tied to a work-item REQ/CHG |

## Context

A comparison against `github/spec-kit` (Spec-Driven Development toolkit)
surfaced its `constitution` pattern: a standing, up-front principles artifact
that later phases (`specify`, `plan`, etc.) are checked against.

The live concern, raised directly: constitution files observed in the wild
(spec-kit-adjacent and otherwise) have grown to 900+ lines of standing
instruction. This harness already carries a compact principles document
(`CLAUDE.md`, 9 numbered sections) that every session loads automatically —
though on inspection it blended durable principle with operating mechanics
(exact verify commands, log line formats, a slash-command reference list),
which is itself an early symptom of the same accretion pattern: procedure
tends to get appended to whatever file is already "the rules." Adding a
second, larger "constitution" artifact on top of that risks: (a) two sources
of truth for project principles that drift apart, (b) context/token cost paid
on every session regardless of relevance, (c) a document that accretes
indefinitely because nothing prunes it — the exact failure mode observed
elsewhere.

If we don't decide anything here, `CLAUDE.md` keeps blending principle and
procedure, and the next comparison to another tool will raise the same worry
unresolved.

## Options considered

### Option A — Adopt spec-kit's pattern: new `CONSTITUTION.md`, freestanding

- Sketch: create a new top-level `docs/harness/CONSTITUTION.md`; `IDEA.md`/
  `CHANGE.md` templates gain a field requiring authors to state which
  constitution principles the work item touches.
- Pros: matches spec-kit's shape directly; a single named artifact is easy to
  point newcomers at; separates "durable principles" from "operating
  procedure" (`CLAUDE.md` mixes both today).
- Cons: exactly the bloat risk raised — nothing bounds its growth, and every
  future rule gets added here by default because it's the "principles" file;
  duplicates `CLAUDE.md` §1–9, which already is the durable-principles
  document; two files now need to agree forever.
- Risks: drift between `CONSTITUTION.md` and `CLAUDE.md`; the 900+ line
  failure mode repeats here on a 12–24 month horizon.

### Option B — No new artifact; do nothing

- Sketch: leave `CLAUDE.md` as-is, make no changes.
- Pros: zero new maintenance surface, zero drift risk.
- Cons: leaves real gaps unaddressed — nothing today requires new work items
  to explicitly check themselves against the standing principles the way
  spec-kit's constitution-citation pattern does; `CLAUDE.md`'s content is
  enforced by convention only, not referenced by name from
  `IDEA.md`/`CHANGE.md`.
- Risks: the underlying gap (principles exist but aren't actively cited during
  intake) persists.

### Option C — Treat `CLAUDE.md` as the constitution; split principle from procedure now, don't defer it

- Sketch: no new "constitution" document. Instead, `CLAUDE.md` itself is
  restructured immediately: mechanics (session-start steps, verify-loop
  commands/pipeline, milestone task-size threshold, DECISIONS.log line format,
  the slash-command reference list) are extracted into a new
  `docs/harness/OPERATING-PROTOCOL.md`, mirroring `CLAUDE.md`'s section
  numbers and cross-referenced from each. `CLAUDE.md` keeps only the
  non-negotiable *why* — types-as-contract, data-handling hard limits,
  segregation of duties, brownfield discipline, escalation rules — plus a
  one-line pointer to the protocol doc per section. `templates/IDEA.md` and
  `templates/CHANGE.md` gain a required "Constitution sections consulted"
  field, forcing intake to actively cite `CLAUDE.md` rather than assume
  familiarity. A ~150-line soft ceiling is stated in `CLAUDE.md` itself as a
  self-check: if it's approached, that's the signal procedure crept back in.
- Pros: solves the actual problem (principles cited at intake, not just
  ambiently present) without a second *constitution* document; fixes the
  principle/procedure blend immediately instead of accepting it as
  known-debt — `OPERATING-PROTOCOL.md` can now change (new commands, new
  pipeline steps) without touching `CLAUDE.md` at all, which is the real
  long-term bloat defense, not just a line-count warning; zero drift between
  two "principles" documents because there's still only one.
- Cons: two files now exist instead of one (`CLAUDE.md` +
  `OPERATING-PROTOCOL.md`), so there's a new question of which file new
  content belongs in — mitigated by a clear test (does this change if
  tooling changes, independent of *why* we do it? → protocol; is it a
  standing non-negotiable? → constitution); one-time restructuring cost paid
  now rather than deferred.
- Risks: misfiled future additions (a procedural detail added to `CLAUDE.md`
  out of habit) slowly re-blend the two documents if nothing checks it at
  retro.

## Decision

**Option C — executed, not deferred.** `CLAUDE.md` is declared the
constitution — no second file. Its procedural content has already been split
out to the new `docs/harness/OPERATING-PROTOCOL.md` (session-start steps,
verify-loop commands/pipeline, milestone task-size threshold, DECISIONS.log
format, ADR/ticket template pointers, slash-command reference), leaving
`CLAUDE.md` at 113 lines of principle-only content plus one-line pointers to
the protocol doc per section. `CLAUDE.md` states its own ~150-line soft
ceiling as a self-check. "Constitution sections consulted" is now a required
field in `IDEA.md` and `CHANGE.md`.

This directly answers the concern raised: the 900-line failure mode happens
when a constitution file has no owner, no ceiling, and no separation from
procedure — material of the wrong altitude gets appended because there's
nowhere else for it to go. Removing that "nowhere else" by giving procedure a
real home (`OPERATING-PROTOCOL.md`) is a stronger defense than a line-count
warning alone would have been.

AI recommendation: Option C, for the reasons above — it was chosen over
Option A specifically because Option A reproduces the maintenance-surface risk
that prompted this ADR (a second document that can independently bloat),
rather than because "new artifact" is wrong in general.

## Consequences

**Easier:** principles get actively cited (not just ambiently trusted) at
intake; `OPERATING-PROTOCOL.md` can absorb new commands, pipeline steps, or
log formats without touching `CLAUDE.md` at all — the actual long-term bloat
defense.

**Harder / new commitments:** two files now exist where there was one — future
authors must judge which document new content belongs in (durable *why* vs.
changeable *how*); `CLAUDE.md`'s ~150-line self-check needs a human or retro
to actually notice if breached, or it's theater.

**Tripwire to revisit this ADR:** if `CLAUDE.md` approaches ~150 lines again
despite the split (i.e., procedure is creeping back in rather than going to
`OPERATING-PROTOCOL.md`), that's the signal to reopen this ADR at the next
retro — not to create a third document, but to check whether the two-file
split test itself needs sharpening.
