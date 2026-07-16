---
name: harness-prd
description: Stage 01 — turn an approved idea into a PRD with numbered testable REQ-### requirements, non-goals, and a data inventory, targeting gate G1.
---

# harness-prd

Playbook: `stages/01-discovery.md`. Template: `templates/PRD.md`. Exit: G1.

Precondition: G0 in `DECISIONS.log`. If absent, say so and offer `/harness-ideate`.

1. Draft the PRD from `IDEA.md`, assigning `REQ-###` IDs (functional 0xx,
   non-functional 1xx, AI-behavior 2xx). These IDs thread through commits, tests,
   and ADRs for the life of the project — never renumber, only deprecate.
2. Rewrite every requirement until **testable as written**: "fast" → "p95 < Nms at
   R rps"; "secure" → named controls. Given/When/Then for acceptance criteria.
3. Hunt the unstated: error paths, empty states, concurrency, retention, timezones,
   **rounding** (in finance, rounding is a requirement). Ask; don't invent — every
   REQ needs a named source, and a requirement no stakeholder asked for is scope
   creep with a serial number.
4. Build the **data inventory** table: element, classification, source of truth,
   retention, enters-prompts?. Flag anything above the `max_prompt_classification`
   ceiling in `harness.config.yaml` immediately.
5. Draft explicit **non-goals** and confirm them with the user.
6. Park unresolved items in Open Questions with owners; requirements live in this
   document, not in chat.
7. Save `docs/harness/PRD.md`, update `STATE.md`, then state what G1 needs:
   human lock, business-owner approval on T1, `DECISIONS.log` line.
