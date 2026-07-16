---
name: harness-recon
description: Brownfield reconnaissance (Stage B1) — map the existing code with file:line evidence, inventory implicit contracts and consumers, pin current behavior with characterization tests, targeting gate GC. Use after /harness-change, before touching any code.
---

# harness-recon

Playbook: `stages/B1-reconnaissance.md`. Template: `templates/RECON.md`. Exit: GC →
rejoin standard pipeline at Stage 04 (`/harness-build`).

Iron rule: **every claim about existing behavior cites file:line or a test.** If you
can't cite it, trace it until you can — no claims from memory or plausibility.

1. Read the active `CHANGE.md`; create `RECON.md` beside it.
2. **Trace the call path** of the touched behavior end-to-end; record entry points,
   the path in order, state touched, and config/flags that alter it — all with
   file:line references.
3. **Hunt consumers**, especially unglamorous ones: grep the repo, but also ask the
   user about cron jobs, downstream services, report extracts, dashboards — the
   out-of-repo consumers only humans know about.
4. **Inventory implicit contracts** (Hyrum's law): ordering, rounding modes, error
   shapes, timezone handling, null-vs-empty, retry semantics. Present the "safe to
   change?" column to the human — that's their judgment call, not yours.
5. **Characterization tests**: where the touched path has thin coverage, write tests
   pinning *current* behavior — including behavior that looks wrong (pin it, log the
   fix as a proposal; don't fix it inside this change). They must pass against
   unchanged code; run `scripts/verify.sh` to prove it.
6. Check behavior claims against the **lockfile's pinned versions**, not memory.
7. **Archaeology**: significant undocumented decisions in touched code get a
   retroactive ADR describing the status quo — only for what this change touches.
8. Correct CHANGE.md's blast radius, re-answer the escalation triggers, write the
   go/no-go recommendation, update `STATE.md`.
9. Run `scripts/gate-check.sh GC CHG-###` and state what remains for human GC
   approval. On pass → `/harness-build`; commits reference `CHG-###`.
