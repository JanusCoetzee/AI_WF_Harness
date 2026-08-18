# ADR-014 — A ticket precedes any feature, significant/platform bug, or discrete task; routine build-time findings don't need one

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-08-19 |
| Deciders | janus (Driver) |
| REQs served | constitution/traceability discipline itself |

## Context

`#32`'s build found two real defects live, both fixed forward in the same
commit:

1. `build_manifest()` also needs `harness.config.yaml` from
   `HARNESS_ROOT` — a small, local fix, entirely in service of making
   `#32`'s own already-ticketed acceptance criteria actually pass. No new
   capability, no platform-level change, nothing a future reader would
   need to discover independently of `#32` itself.
2. Git's "dubious ownership" check rejects `git rev-parse` on root-owned
   content — required a platform-level fix (`git config --system --add
   safe.directory`, a container-wide config change affecting how *every*
   process resolves git provenance, in both content modes) and was named
   at the time as **"a latent risk for `#31`'s already-shipped, already-
   closed container."**

The Driver asked whether either got its own GitHub issue. Neither did —
both were fixed, then documented in `#32`'s own `CHANGE.md`/
`DECISIONS.log` after the fact. `#34` was filed for finding #2, but only
once asked, and only *after* the fix was already written and committed
(`5b9f61e`) — a ticket reverse-engineered from work already done, not a
ticket that authorized the work before it happened. That's the real gap:
not "does a ticket eventually exist" but **"did the ticket precede the
work, the way `CLAUDE.md` §5 already says it should"** ("the ticket is
the prompt").

A first draft of this ADR proposed a test based on whether a finding
*reaches outside the active ticket's own scope*. The Driver corrected
that framing directly: reach isn't the right axis. **Findings during
build are normal** — engineering flow, not a compliance gap, and
ticketing every one of them (even ones that touch other work, if they're
small and routine) would recreate the exact bureaucracy this repo's own
retro discipline already guards against. The actual line is about the
**nature of the work**, not which ticket's blast radius it happens to
fall inside: a feature, a significant bug requiring a platform-level
change, or a specific, plannable task needs a ticket *before* it starts.
A small correction discovered and fixed in service of already-ticketed
work does not, before or after.

## Options considered

### Option A — Status quo: document findings in the active ticket's own CHANGE.md/DECISIONS.log, file a separate ticket only when the finder judges it warrants one

- Sketch: no new rule. Continue as this session did.
- Pros: zero added ceremony.
- Cons: no sequencing discipline at all — a ticket, if filed, is filed
  whenever the finder gets around to it, which in practice meant *after*
  the fix, when asked. That's a receipt, not a prompt.
- Risks: recurs identically; the issue tracker depends entirely on
  someone remembering to ask.

### Option B — Strict: every finding gets its own ticket, filed and referenced before any code is written, no exceptions

- Sketch: mid-build discovery of anything — including a one-line fix
  needed to make the active ticket's own acceptance criteria pass — stops
  work until a ticket exists for it.
- Pros: maximal sequencing discipline, zero ambiguity.
- Cons: **this is exactly the ticketing overhead the Driver explicitly
  rejected.** "Findings issues as part of build is normal" — stopping a
  build to ticket a one-line fix that's already in service of an
  existing ticket's own stated work is bureaucracy with no real payoff;
  nobody would ever need `#32`'s `harness.config.yaml` fix to have its
  own ticket to find it.
- Risks: the rule gets ignored in practice because it's too heavy to
  actually follow, which is worse than not having it — an unenforced
  rule teaches that rules in this document are optional.

### Option C — By kind, not by reach: a ticket precedes a feature, a significant/platform-level bug fix, or a discrete task; routine build-time findings-and-fixes don't need one, before or after

- Sketch: the test is what *kind* of work this is, decided at the moment
  it's found:
  - **Feature** — new capability. Always needs a ticket first.
  - **Significant bug** — one whose fix is a platform/architecture-level
    change (new config, new dependency, altered behavior of a shared
    mechanism) rather than a local one-liner. Needs a ticket first, even
    if it's discovered mid-build on something else. Finding #2
    (`git config --system`, a container-wide behavior change touching
    both content modes and a different, already-shipped ticket) is this
    case — it should have been ticketed *before* the fix was written,
    not after.
  - **Specific task** — a deliberate, plannable unit of work someone
    would reasonably ask "did that happen yet?" about. Needs a ticket
    first.
  - **Routine build-time finding** — a small correction discovered and
    fixed in direct service of the active ticket's own already-stated
    acceptance criteria (finding #1: `#32` already promised baked mode
    would work; making it actually work isn't new, unticketed work).
    No ticket needed, before or after — this is what "the ticket is the
    prompt" already covers, since the active ticket is the prompt for
    getting its own criteria to pass.
- Pros: matches the Driver's own correction directly — kind, not reach;
  keeps genuine build-time iteration cheap (no stop-the-world for a
  one-liner); still closes the actual gap (`#34` should have preceded its
  fix, and would have under this rule, since a container-wide `git
  config` change is unambiguously a platform-level fix).
- Cons: "significant" still requires judgment at the moment of discovery
  — not fully mechanical.
- Risks: judgment could still under-fire under time pressure, same
  failure mode as Option A. Mitigated by naming concrete examples (this
  ADR's own two findings) as calibration anchors, not just an abstract
  category.

## Decision

**Option C.** Ticket-before-work for anything that's actually work — a
feature, a significant/platform-level bug, or a discrete task. Not for
routine build-time corrections made in service of an already-ticketed
piece of work; those are what building the ticket *is*, not separate
unprompted work riding along with it.

**Calibration, using this session's own two findings as the anchor:**

| Finding | Kind | Ticket needed? | When |
| --- | --- | --- | --- |
| `#32`'s missing `harness.config.yaml` | Local fix, in service of `#32`'s own stated criteria | No | — |
| `#32`'s `git config --system` fix (dubious ownership) | Significant — platform-level config change, affects a different already-shipped ticket (`#31`) | **Yes** | **Before** the fix, not after (`#34` should have preceded `5b9f61e`, not followed it) |

**The corollary that actually closes the gap:** for anything that clears
the "significant/feature/task" bar, *filing the ticket after the fix is
already written is not compliance* — it's the same failure this ADR
exists to end, just with better paperwork. The ticket has to come first,
or it isn't the prompt.

## Contracts (CLAUDE.md wording, defined before implementation)

Proposed addition to `CLAUDE.md` §5 (Traceability), directly after the
existing "Where a real ticket exists..." bullet:

> - **A ticket precedes the work, not the other way round.** Features,
>   significant bugs (ones needing a platform/architecture-level fix —
>   new config, new dependency, altered behavior of a shared mechanism),
>   and discrete tasks get a ticket *before* work starts, even when found
>   mid-build on something else. Routine build-time corrections made in
>   service of an already-ticketed piece of work don't need a separate
>   ticket, before or after — that's normal engineering flow, not a gap
>   (ADR-014).

Keeps `CLAUDE.md` itself terse (one bullet, points to this ADR for the
calibration table) per its own stated ~150-line discipline — the file is
at 123 lines before this addition.

## Consequences

**Easier:** the issue tracker stays a trustworthy *prompt* for
significant work instead of degrading into an occasionally-updated
*receipt*; genuine build-time iteration (the `harness.config.yaml` kind
of fix) stays cheap and unencumbered, matching how the Driver actually
wants to work.

**Harder / new commitments:** the "significant vs. routine" call has to
be made honestly in the moment, under the same time pressure that caused
this gap in the first place — mitigated by the calibration table above,
but not eliminated. Worth a retro check-in after a few real uses
(`templates/RETRO.md`'s AI-pairing audit) to see whether the line held or
drifted either direction.

**Retroactive:** `#34` (2026-08-19) was filed *after* its fix, which is
exactly the sequencing this ADR says not to repeat — left as-is (a late
ticket beats no ticket for something already shipped), but named here
plainly as the example of what "wrong order" looks like, not held up as
a model application of this rule.
