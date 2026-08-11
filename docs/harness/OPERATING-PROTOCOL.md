# Operating protocol — AI Workflow Harness

Mechanics: the concrete steps, commands, and reference lists that implement the
durable principles in `CLAUDE.md`. This document changes as tooling changes;
`CLAUDE.md` should not need to change when this one does. Section numbers below
mirror `CLAUDE.md`'s numbered sections.

## 1. Session start steps

1. Read `docs/harness/STATE.md` (current stage, active work item, risk tier).
   If it doesn't exist, offer to run `/harness-status` to initialize it.
2. Identify which gate is next and what evidence it requires (`gates/GATES.md`).
   Two entry paths exist: the full workflow (G0–G3) for project-sized work, and
   the **brownfield fast path** (`/harness-change` → `/harness-recon` → gate GC)
   for changes to existing code — which is most work. Both rejoin at Stage 04.
3. If the user asks for work that belongs to a *later* stage than the current
   one, say so explicitly and name the missing gate. Proceed only if the user
   overrides — and record the override in `docs/harness/DECISIONS.log`.

## 2. Verify loop — commands and pipeline

Run `scripts/verify.sh` (or the commands under `verify:` in `harness.config.yaml`):

```
typecheck → lint → unit tests → evals (if AI feature) → build
```

Thresholds live in `docs/STANDARDS.md`, configured via `harness.config.yaml`
`standards:` (changed-line coverage, cognitive complexity ceilings, dependency
severity limits).

`lint` also chains `scripts/data-scan.sh` (ADR-007) — a pattern scan for
hardcoded secrets/PII-shaped strings, catching §6 violations at verify time
rather than waiting for the G6 secure gate. Escape hatch for a genuine false
positive: a `# data-scan: allow` comment on the offending line.

## 4. Milestone mechanics

- Task size threshold: if a task exceeds ~half a day of work, stop and split it
  in the plan first.
- After each milestone: run the demo command, then update `STATE.md` progress.

## 5. Traceability mechanics

- `DECISIONS.log` line format: `2026-07-16 | G3 passed | <who> | <link>`.
- Ticket standard: `templates/ISSUE.md` Definition of Ready.
- ADR template: `templates/ADR.md`.

## Slash commands

`/harness-status` `/harness-ideate` `/harness-prd` `/harness-adr` `/harness-plan`
`/harness-issues` `/harness-build` `/harness-review` `/harness-secure`
`/harness-release` `/harness-retro`
Brownfield fast path: `/harness-change` `/harness-recon` (with `/harness-issues`
Mode B for repairing vague inbound tickets)
Lanes: `/harness-maintain` (routine dependency/config hygiene, one batch dossier)
`/harness-breakglass` (emergencies only — human-declared, act-first, retro'd)
