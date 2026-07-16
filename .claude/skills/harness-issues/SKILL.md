---
name: harness-issues
description: Externalize a ratified plan (or repair an inbound ticket) into correct-at-birth Jira/GitHub issues — each a self-contained vertical slice passing the Definition of Ready. The ticket is the prompt; use after /harness-plan, or whenever a ticket is too vague to build from.
---

# harness-issues

Template: `templates/ISSUE.md`. The governing idea (Pocock's `to-issues`): an LLM
session is stateless, so **the ticket must be the complete brief** — correct at the
start, because every downstream stage inherits the ticket's quality.

## Mode A — plan → issues (after G3)

1. Read the ratified `PLAN.md`. For each task (or coherent task cluster), draft one
   issue from `templates/ISSUE.md`:
   - **One vertical slice per issue.** If a task is horizontal ("add repository
     layer"), merge it into the slice that needs it or justify the exception in the
     ticket. The slice table names every layer touched — UI, API contract, backend,
     data, deploy.
   - **Fresh-session test** before creating: could a new session with only this
     ticket + repo do the work? Inline the constraint summaries (don't make the
     reader open three ADRs to learn one sentence); link for depth.
   - Acceptance criteria copied/derived from PLAN and PRD — testable as written,
     with REQ-###/CHG-### refs. Proof command included. Out-of-scope stated.
   - Sized ≤ ~1 day. Split before creating, never after starting.
2. Run every draft against the **Definition of Ready** checklist in the template.
   A draft that fails DoR gets fixed or split — creating it anyway defeats the point.
3. Present all drafts to the user for approval, **then** create:
   - GitHub: `gh issue create` (labels: milestone, tier, `REQ-###`).
   - Jira: via the Atlassian MCP if connected; otherwise emit paste-ready text per
     issue and say so.
   - Creating tickets is outward-facing — never create without explicit go-ahead.
4. **Write ticket keys back** into PLAN.md's task rows. From here the ticket key is
   the traceability handle: commits and PRs reference the Jira key / `#issue`.

## Mode B — inbound ticket repair (brownfield reality)

Most tickets arrive vague ("summary is wrong sometimes"). The first act is fixing
the ticket, not the code:

1. Rewrite the ticket to the ISSUE.md standard — named source, behavior title,
   testable acceptance criteria, blast-radius-aware slice table, out-of-scope.
2. Post the rewrite back to the ticket (comment or description edit, with
   go-ahead) so the *shared* artifact is the corrected one — not a private copy.
3. Hand off: `/harness-change` uses the repaired ticket as its source; the ticket
   key becomes the change ID (use `FIN-4821`, not a parallel `CHG-###`).

## Quality bar (reject your own drafts against this)

- A title naming a component is a smell; a title naming a behavior is the standard.
- "See parent ticket for details" fails the fresh-session test.
- Acceptance criteria that restate the title are not criteria.
- If two issues can't be worked in either order without coordination, the slicing
  is wrong — re-cut.
