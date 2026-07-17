# ADR-001 — The harness browser stays read-only; edits go through git

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-18 |
| Deciders | janus (Driver), on the AI pair's recommendation — Driver ruled "keep as is" |
| REQs served | governance integrity of the harness content itself |

## Context

The browser (app/) renders stages, gates, templates, skills, and evals from the
repo, read-only. Question raised: should flow/content be editable via the UI?

## Options considered

### Option A — "Edit on GitHub" deep links per page

Zero new surface; edits become commits/PRs, so CI (verify + six-scenario eval
regression) and review gates apply automatically. Recommended by the AI pair;
Driver declined even this — the browser stays purely a lens.

### Option B — in-browser editor writing branches/PRs via API

Governed but heavy: auth, branching, conflicts — poor value for a single-user tool.

### Option C — direct working-tree writes from the browser

Rejected on principle: bypasses commit-guard (issue traceability), the
verify-before-done hook (browser writes are invisible to tool hooks), eval
regression timing (breakage lands on the next unrelated commit), and review
gates. The operating model's own rule generalizes: artifacts edited in a
dashboard are artifacts you cannot audit.

## Decision

Read-only stands, with no edit links. All changes to harness content travel the
same path as code: issue → edit → verify → commit → CI → review per tier.

## Consequences

Easier: one audit trail, hooks and eval regression cover every content change.
Harder: no casual in-UI tweaks — deliberate. Tripwire: if multi-user adoption
creates real demand for UI editing, revisit via Option A first, superseding this
ADR on purpose.
