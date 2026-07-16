# Threat Model — PayGuard exception triage

| Field | Value |
| --- | --- |
| Tier | T1 (full STRIDE) |
| Reviewed by | Risk/Sec partner (drill placeholder) |
| Date | 2026-07-17 |

## System sketch

```text
[payments hub] --kafka--> [triage-svc] --https--> [redaction svc] --> [LLM gateway]  <- trust boundary
                              |--> [recommendation store] --> [case tool UI] --> [analyst]
```

## STRIDE per trust boundary

| Boundary | S | T | R | I | D | E | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hub → triage-svc | topic ACLs | schema-validated events | offset log | Confidential payload at rest | consumer lag | n/a | mTLS, schema registry, encrypted topic | REQ-103 |
| triage-svc → gateway | svc identity | prompt/response signing n/a — TLS | request log w/ model+prompt version | **PII leakage — redaction before boundary** | gateway quota | prompt scope | redaction svc, EU-region gateway only, no public APIs | REQ-202, data inventory |
| store → case tool | UI auth | recommendation immutable once written | analyst action log | role-based views | n/a | analyst-only actions | case tool RBAC | REQ-003/004 |

## AI-specific threats

| Threat | Applies? | Mitigation | Verified at G6? |
| --- | --- | --- | --- |
| Prompt injection via untrusted input (remittance free text is attacker-writable by any payment sender) | **Yes — primary threat** | Redacted, demarcated input blocks; instructions never sourced from data; output schema allowlist of 6 categories; injection eval 100% floor | pending |
| Sensitive data leakage into prompts/provider logs | Yes | Redaction service before gateway; counterparty fields never sent; gateway is EU-region, no-retention contract | pending |
| Unsafe output handling | Yes | Output is a category enum + confidence, schema-validated; never executed or interpolated; invalid ⇒ manual queue (REQ-006) | pending |
| Excessive agency | Yes | Model recommends only; case moves solely on analyst approval (REQ-003); no tool access from the model | pending |
| Model/prompt drift degrading a control | Yes | Pinned versions; eval regression gate; weekly online sampling vs eval floors | pending |
| Denial of wallet | Yes | Per-day call budget = 2× expected volume; alert at 80% | pending |

## Assumptions & accepted risks

| # | Assumption / accepted risk | Owner | Expiry |
| --- | --- | --- | --- |
| 1 | Approved gateway's no-retention contract holds | Risk partner | review 2027-01 |
