# Stage B0 — Change Intake (brownfield fast path)

**Purpose:** Frame a change to existing code in one page, tier it, and decide whether
the fast path is legitimate — before any code is read in anger. Exit: **GC** (jointly
with B1 recon).

Most day-to-day engineering is this: a bug fix, a small feature, a config change, a
dependency bump on a platform that already exists. The full IDEA→PRD→ADR→PLAN run
would be ceremony-theater here. The fast path replaces G0–G3 with a single gate — but
it earns that compression by being honest about **escalation triggers**.

## Inputs

A ticket, a bug report, an ask — with a **named source**. "Someone mentioned" is not
a source.

## LLM role

- Create `docs/harness/changes/CHG-###/CHANGE.md` (next free number) from the template.
- Interrogate the intent down to two sentences and **testable acceptance criteria**
  (`CHG-###.n`). A bug fix's first criterion is usually "the failing case, as a test".
- Propose the **risk tier for the change, not the codebase** — a typo fix in a
  payments repo is not T1; a "small" retry tweak on a money-moving path is.
- Draft the blast-radius estimate and answer the four **escalation triggers**
  honestly. Recommending escalation to the full workflow is a success of the fast
  path, not a failure.
- Write the rollback note. If rollback is genuinely "revert the commit", say why
  that's true (no migration, no config, no adapting consumer).

## Human role

- Confirm tier and source; supply the institutional context (freeze windows,
  adjacent in-flight work, political landmines around the touched system).
- T1 changes: a peer co-signs the intake itself.

## Outputs

- `docs/harness/changes/CHG-###/CHANGE.md` — then straight into **B1 Reconnaissance**.
  Only docs/typo-level trivia may waive recon, and the waiver is written down.

## Anti-patterns

- Tiering by repo instead of by change — in both directions.
- Acceptance criteria that restate the ticket title instead of pinning behavior.
- Using the fast path for what is actually a project. The 3-day trigger exists
  because "small changes" that run for weeks are unplanned projects.
