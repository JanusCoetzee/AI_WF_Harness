# Threat Model — <work item name>

| Field | Value |
| --- | --- |
| Tier | T1 (full STRIDE) / T2 (boundary table only) |
| Reviewed by | <Risk/Sec partner for T1> |
| Date / Delta-reviewed at G6 | |

## System sketch

Components, trust boundaries, data flows. ASCII diagram is fine — what matters is that
every boundary drawn here appears in the table below.

```text
[User] --https--> [API GW] --> [Service] --> [DB]
                                  |--> [LLM provider]   <- trust boundary!
```

## STRIDE per trust boundary

| Boundary | S(poofing) | T(ampering) | R(epudiation) | I(nfo disclosure) | D(oS) | E(levation) | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## AI-specific threats (mandatory if any LLM in the flow)

| Threat | Applies? | Mitigation | Verified at G6? |
| --- | --- | --- | --- |
| Prompt injection via untrusted input (user text, retrieved docs, tool results) | | Input demarcation, output validation, no instructions from data | |
| Sensitive data leakage into prompts / provider logs | | Data inventory ceiling, redaction layer | |
| Unsafe output handling (exec, SQL/HTML interpolation, auto-actions) | | Schema validation; output treated as untrusted | |
| Excessive agency (model can cause more than the feature needs) | | Tool allowlist, rate/spend limits, human checkpoint per tier | |
| Model/prompt drift degrading a control | | Pinned versions, eval regression gate, online monitoring | |
| Denial of wallet (cost amplification) | | Budget alarms, per-caller quotas | |

## Control failure semantics

For every *control* in the modeled flow (screening, authorization, validation,
limits): what happens when the control itself fails? **Fail-open or fail-closed is
a named decision with an owner** — never an emergent property of timeout handling.

| Control | On failure: open / closed | Consequence accepted | Decided by |
| --- | --- | --- | --- |

## Assumptions & accepted risks

| # | Assumption / accepted risk | Owner | Expiry / revisit date |
| --- | --- | --- | --- |
