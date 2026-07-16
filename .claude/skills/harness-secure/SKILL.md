---
name: harness-secure
description: Stage 06 — run the security and compliance checklist (secret scan, dep audit, threat-model delta, data sweep, AI checks), targeting gate G6.
---

# harness-secure

Playbook: `stages/06-security-compliance.md`. Exit: G6.

Precondition: G5 in `DECISIONS.log`.

Run the mechanical checks and draft the judgment calls; record everything in
`docs/harness/secure-gate-record.md`:

1. **Secret scan** over branch history (gitleaks/trufflehog if available; otherwise
   targeted grep for key patterns and say the scan was degraded). Found secret →
   stop everything; rotation comes before scrubbing.
2. **Dependency audit** per ecosystem. Draft waiver text (with expiry) for anything
   the human chooses to accept — you never accept risk yourself.
3. **Threat-model delta** — the highest-value check: re-read `THREAT-MODEL.md`
   against the code as built. List every endpoint, queue, data flow, or tool-call
   the model gained that the threat model never saw. Model them now.
4. **Data sweep**: grep fixtures, logs, error messages, telemetry for realistic
   account numbers, names, credentials. Synthetic-only is a G6 condition.
5. **AI-feature checks** (if applicable): verify the injection mitigations the
   threat model claimed; confirm output is schema-validated and never executed or
   interpolated; confirm tool allowlists/limits match "least agency"; confirm eval
   evidence is current for the pinned model+prompt.
6. Draft the **change record** text for the institution's change system (T1/T2).
7. Report findings ranked by severity, including anything found *outside* this
   change's scope. State what G6 needs: Risk/Sec partner judgment on T1.
