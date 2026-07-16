# Stage 06 — Security & Compliance

**Purpose:** Confirm what was built matches what was threat-modeled, and clear the institutional bar. Exit: **G6**.

## Checklist (evidence for each item goes in `docs/harness/evidence/`)

1. **Secret scan** across the full history of the branch (e.g. gitleaks/trufflehog).
   A found secret = rotate first, then scrub; never just delete the line.
2. **Dependency audit** (`npm audit` / `pip-audit` / SCA tool). Critical/High findings
   are fixed or formally waived with an expiry date — no evergreen waivers.
3. **Threat-model delta:** re-read `THREAT-MODEL.md` against the code as built.
   New endpoints, queues, or data flows that weren't modeled get modeled now.
4. **Data-handling sweep:** grep fixtures, logs, error messages, and telemetry for
   anything resembling real customer data, account numbers, or credentials.
5. **AI-feature checks** (if applicable):
   - Prompt injection: untrusted input reaching a prompt is treated as hostile;
     verify the mitigations that the threat model claimed.
   - Output handling: model output is schema-validated and never executed,
     interpolated into SQL/HTML, or granted authority without checks.
   - Least agency: the model can only *cause* what the feature needs (tool
     allowlists, spending/rate limits, human checkpoints per tier).
   - Eval evidence current for the pinned model+prompt versions.
6. **Change record** raised in the institution's change-management system (T1/T2),
   linking to the evidence bundle.

## LLM role

Run the mechanical checks, draft the delta analysis and waiver requests, prepare the
change-record text. Flag anything it finds *even when unrelated to this change*.

## Human role

Risk/Sec partner judges the findings (T1); Driver walks the checklist with sign-off (T2).
Only a human grants a waiver.

## Anti-patterns

- Treating G6 as a scan-runner. The valuable check is #3 — the delta between the
  modeled system and the built one.
- Waivers without expiry dates. Risk accepted forever is risk forgotten.
