---
name: harness-change
description: Brownfield fast path entry (Stage B0) — frame a change to existing code in a one-page CHANGE.md with tier, testable acceptance criteria, blast radius, and escalation triggers, targeting gate GC. Use for bug fixes, small features, config changes, and dependency bumps on existing platforms.
---

# harness-change

Playbook: `stages/B0-change-intake.md`. Template: `templates/CHANGE.md`. Exit: GC
(jointly with `/harness-recon`).

0. **Ticket first.** If the inbound Jira/GitHub ticket is too vague to build from,
   repair it via `/harness-issues` Mode B and post the repair back — the ticket must
   be correct before anything else happens. Where a real ticket exists, its key IS
   the change ID (`FIN-4821`, `#123`); only invent a `CHG-###` when no ticket exists.
1. Create `docs/harness/changes/<ID>/CHANGE.md` from the template (ID = ticket key,
   or next free `CHG-###` from `docs/harness/changes/`).
2. Interrogate the ask down to a two-sentence intent with a **named source**.
   For a bug: the first acceptance criterion is the failing case, as a test.
   Number criteria `CHG-###.n` — commits and tests will reference them.
3. Tier **the change, not the codebase**: a typo fix in a payments repo isn't T1;
   a "small" retry tweak on a money-moving path is. Rationale goes in the doc.
4. Draft the blast-radius estimate (modules, consumers, data + classification,
   deploy surface) and the rollback note — "revert the commit" only with the
   justification the template demands.
5. Answer all four **escalation triggers** honestly. Any "yes" → recommend exiting
   to the full workflow at the named gate; that's the fast path succeeding.
6. Fill the FinServ-critical fields the template demands: **linked records** (does
   this close an audit finding or incident? check, don't assume "none"), **timing
   constraints** (freeze windows, batch/statement cycles), and **remediation of
   past impact** — if the defect produced wrong figures or documents historically,
   the disposition of the past is part of the change, not someone else's problem.
7. Recon is next (`/harness-recon`) unless the change is docs/typo-level trivia —
   then mark `waived-trivial` with a written reason.
8. Update `STATE.md` (stage B0, active change). State what GC needs:
   `scripts/gate-check.sh GC CHG-###`, sign-off per tier (T1 adds a peer on the
   intake), `DECISIONS.log` line. You approve nothing.
