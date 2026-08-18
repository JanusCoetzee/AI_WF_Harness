# ADR-014 — A defect or decision that reaches outside its own ticket's scope gets its own ticket, filed when found

| Field | Value |
| --- | --- |
| Status | Proposed |
| Date | 2026-08-19 |
| Deciders | janus (Driver) |
| REQs served | constitution/traceability discipline itself |

## Context

`#32`'s build found two real defects live, both fixed forward in the same
commit and documented in `#32`'s own `CHANGE.md`/`DECISIONS.log`:

1. `build_manifest()` also needs `harness.config.yaml` from
   `HARNESS_ROOT` — scoped entirely to `#32`'s own new, not-yet-shipped
   baked-content mode. No prior shipped behavior broke.
2. Git's "dubious ownership" check rejects `git rev-parse` on root-owned
   content — reproduced for `#32`'s baked mode, but named as **"a latent
   risk for mount mode too"**, meaning it potentially affects `#31`'s
   *already-shipped, already-closed* container. It was fixed forward in
   `#32`'s commit anyway, because the same `Dockerfile` serves both
   modes.

The Driver asked, correctly, whether either got its own GitHub issue.
Neither did — both were documented in prose (`CHANGE.md`,
`DECISIONS.log`) but only the first genuinely belongs there. The second
is a defect in different, already-closed work, discovered as a side
effect of unrelated work, and fixed without ever giving `#31` — the
ticket it actually concerns — any trace of it. Someone auditing `#31` by
reading `#31` (its issue, its `CHANGE.md`, its `DECISIONS.log` lines)
would never find out this happened. `DECISIONS.log` is a flat,
append-only file; finding this fix requires already knowing to look, not
being able to query for it the way an issue tracker's labels/state
allow.

This session already established the shape of the fix (`#34`, filed
retroactively) — this ADR is about making it systematic instead of
depending on the Driver noticing and asking each time.

## Options considered

### Option A — Status quo: document findings in the active ticket's own CHANGE.md/DECISIONS.log, file a separate ticket only when the finder judges it warrants one

- Sketch: no new rule. Continue as this session did.
- Pros: zero added ceremony; fastest for genuinely self-contained findings.
- Cons: **this is the exact gap that just produced an undiscoverable fix
  to `#31`.** Judgment calls about "does this warrant its own ticket"
  are made by whoever's mid-build on something else entirely, under time
  pressure, with an obvious incentive to just keep going — precisely the
  condition most likely to under-file.
- Risks: recurs identically the next time a fix rides along with an
  unrelated ticket's commit; the issue tracker silently stops being a
  complete record, only `DECISIONS.log` (unqueryable, append-only) is.

### Option B — Strict: every distinct finding, no matter how small or how scoped, gets its own ticket

- Sketch: any defect or decision, including ones fully contained within
  the active ticket's own not-yet-shipped scope (like finding #1 above),
  gets a separate GitHub issue before or as it's fixed.
- Pros: maximally complete audit trail, no judgment call required, ever.
- Cons: directly contradicts this repo's own stated anti-bureaucracy
  principle (`templates/RETRO.md`'s ceremony audit: "A harness that only
  grows becomes the bureaucracy it replaced") and the existing
  `recon: waived-trivial` allowance for docs/typo-level work. Filing a
  ticket for every sub-finding inside an active build — including things
  like finding #1, which no future reader would ever need to discover
  independently of `#32` itself — is noise, not traceability.
- Risks: the tracker fills with tiny, low-value tickets; real findings
  (like finding #2) get lost in that noise instead of standing out.

### Option C — Scoped rule: a finding gets its own ticket only if it reaches outside the active ticket's own not-yet-shipped scope; findings fully contained within it stay documented in-ticket

- Sketch: the test is not "how big is the finding" but **"would a future
  reader need to discover this by reading a ticket other than the one
  I'm currently working?"** Findings entirely within the active ticket's
  own new, not-yet-shipped work (finding #1: new code this same ticket
  is introducing) stay documented in that ticket's `CHANGE.md`/
  `DECISIONS.log`, no new ticket. Findings that touch already-shipped/
  closed work, a different subsystem, or anything outside the active
  ticket's own blast radius (finding #2: a defect in already-closed
  `#31`) get their own ticket, filed when found — even if immediately
  closed alongside the fix, same as any other gate in this repo.
- Pros: draws the line exactly where this session's actual gap was —
  matches the Driver's own follow-up question precisely (they didn't
  flag finding #1, only asked once finding #2's cross-ticket nature was
  explained); keeps the anti-bureaucracy principle intact for genuinely
  self-contained build-time findings; makes the issue tracker complete
  for the cases that actually matter for audit — cross-cutting, latent,
  or already-shipped defects.
- Cons: still a judgment call ("does this reach outside the active
  ticket's scope") — not fully mechanical, unlike Option B.
- Risks: the judgment call could be under-applied the same way Option A's
  was, if not paired with an explicit, checkable test rather than a vibe.
  Mitigated by stating the test as a concrete question (below), not a
  general exhortation to "use good judgment."

## Decision

**Option C.** It closes the actual gap this session found without
recreating the bureaucracy problem this repo's own retro discipline
already guards against. The concrete, checkable test (not a vibe):

> **Would a future reader auditing the ticket this finding actually
> concerns — not the ticket you happen to be working — discover it by
> reading only that ticket's own `CHANGE.md`/issue/`DECISIONS.log`
> lines?** If no, it gets its own ticket, filed when found.

Corollary, stated plainly: **a fix riding along in an unrelated ticket's
commit is not, by itself, traceability** — traceability means the ticket
the finding actually concerns has a trace to it, not that a trace exists
*somewhere* in the repo's history for someone who already knows to look.

**Scope note, so this doesn't collapse into Option B by accident:** the
test is about *reach*, not *size*. A one-line fix that reaches outside
its active ticket's scope still gets a ticket; a large finding fully
contained within the active ticket's own new work still doesn't need
one. `recon: waived-trivial`'s existing docs/typo-level exception is
unaffected — this ADR governs *code defects and cross-cutting
decisions*, not documentation trivia.

## Contracts (CLAUDE.md wording, defined before implementation)

Proposed addition to `CLAUDE.md` §5 (Traceability), directly after the
existing "Where a real ticket exists..." bullet:

> - **No work without a ticket.** A defect or decision found while
>   building one ticket gets its own ticket, filed when found, if a
>   future reader auditing the *other* work it concerns wouldn't
>   discover it from that work's own record — even if closed immediately
>   alongside the fix. Findings fully contained within the active
>   ticket's own not-yet-shipped scope stay documented there; this isn't
>   a ticket for every sub-step (ADR-014).

This keeps `CLAUDE.md` itself terse (one bullet, points to this ADR for
the reasoning/test) per its own stated ~150-line discipline — the file
is at 123 lines before this addition.

## Consequences

**Easier:** the issue tracker becomes a genuinely complete record for the
cases that matter — cross-cutting and latent defects, not just whatever
ticket happened to be open when they were found; future audits of a
closed ticket can trust that ticket's own record instead of needing to
search all of `DECISIONS.log` for stray mentions.

**Harder / new commitments:** every session doing build work now carries
an explicit, checkable test to apply mid-build, not just a general
instinct — a small but real interruption to flow; the line between
Option C and Option B (reach vs. size) has to be actually applied
consistently, not just stated once and forgotten, or this drifts back
toward either extreme over time. Worth a retro check-in item
(`templates/RETRO.md`'s AI-pairing audit) after a few real uses, the same
way ADR-011's override use-count was tracked rather than assumed fine.

**Retroactive:** `#34` (this session, 2026-08-19) is the first
application of this rule, filed before the ADR that names the rule was
even ratified — the gap was real and worth closing immediately, not
waiting for ceremony to catch up with itself.
