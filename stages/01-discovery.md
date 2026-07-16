# Stage 01 — Discovery

**Purpose:** Convert the approved idea into testable, numbered requirements. Exit: **G1**.

## Inputs

`IDEA.md` (G0 passed), stakeholder access, existing system docs.

## LLM role

- Draft the PRD from `templates/PRD.md`, assigning `REQ-###` IDs — these IDs are the
  spine of traceability for the rest of the project.
- Rewrite every requirement until it is **testable as written**. "Fast" becomes
  "p95 < 300ms at 50 rps". "Secure" becomes specific controls.
- Hunt for the unstated: error paths, empty states, concurrency, retention, timezone,
  rounding (in finance, rounding is a requirement, not a detail).
- Build the **data inventory**: every data element touched, its classification, its
  source of truth. Flag anything above the prompt ceiling immediately.
- Propose explicit **non-goals** — the cheapest scope control that exists.

## Human role

- Own conversations with stakeholders; the LLM preps questions, the human asks them.
- Arbitrate conflicts between requirements; the PRD records the ruling.
- Approve G1 with the business owner (T1).

## Outputs

- `docs/harness/PRD.md` — numbered REQs, acceptance criteria, non-goals, data inventory.

## Anti-patterns

- Requirements that live in chat/email instead of the PRD. If it's not a `REQ-###`,
  it will not be built, tested, or defensible later.
- Letting the LLM invent plausible-sounding requirements no stakeholder asked for —
  every REQ needs a named source.
