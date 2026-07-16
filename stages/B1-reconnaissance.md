# Stage B1 — Reconnaissance (brownfield fast path)

**Purpose:** Understand the code before changing it. Map what's really there, find
the implicit contracts, and pin current behavior with characterization tests. Exit:
**GC** → rejoin the standard pipeline at Stage 04.

This is where an LLM pair earns its keep in brownfield work — and where it is most
dangerous if undisciplined. The rule: **every claim about existing behavior cites
`file:line` or a test.** No claims from memory or plausibility.

## LLM role

- **Trace, don't skim.** Walk the actual call path of the behavior being changed;
  record it in `RECON.md` with file:line references. Grep for callers, including
  the unglamorous consumers: cron jobs, other services, report extracts, deploy
  configs, that one dashboard query.
- **Inventory implicit contracts** (Hyrum's law): ordering, rounding modes, error
  shapes, timezone handling, null-vs-empty, retry semantics. In a bank, someone's
  reconciliation spreadsheet depends on at least one of these.
- **Characterization tests before change** (the Feathers rule — legacy code is code
  without tests): where coverage on the touched path is thin, write tests that pin
  *current* behavior — including current behavior that looks wrong. They must pass
  against unchanged code; changing a pinned behavior then becomes a visible,
  deliberate diff to a test, not a silent side effect.
- **Verify against the pinned versions in the lockfile**, not training memory —
  the deployed framework version's behavior is the truth.
- **Archaeology rule:** significant undocumented decisions discovered in touched
  code get a retroactive ADR describing the status quo. Only for what you touch —
  no estate-wide dig.
- Correct CHANGE.md's blast radius and re-answer the escalation triggers with what
  recon revealed. If the change grew: recommend escalation. Then Go/No-go.

## Human role

- Review the code map against institutional knowledge — the consumers and history
  that live in people's heads, not the repo.
- Rule on "safe to change?" for each implicit contract. That's a judgment about
  who's out there, not about the code.
- Approve GC (`scripts/gate-check.sh GC CHG-###`, sign-off per tier, DECISIONS.log).

## Outputs

- `docs/harness/changes/CHG-###/RECON.md`, characterization tests in the test tree,
  retro-ADRs if any. Then **Stage 04** with the standard loop; commits reference
  `CHG-###`; G4–G7 apply per tier.

## Anti-patterns

- "Recon by reading the diff of my intended change." Recon maps what exists, not
  what you plan.
- Fixing "obviously wrong" behavior discovered during recon, inside this change.
  Pin it, log it as a proposal, keep the change's scope.
- Letting characterization tests morph into aspiration tests. They document what
  *is*; the change commit is where behavior moves.
