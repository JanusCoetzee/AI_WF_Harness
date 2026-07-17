# Threat Model — real-time sanctions screening

| Field | Value |
| --- | --- |
| Tier | T1 (full STRIDE) |
| Reviewed by | Risk/Sec partner (drill placeholder) |
| Date | 2026-07-17 |

## System sketch

```text
[payments hub] --> [intake svc] --https--> [VerifyChain API]   <- vendor trust boundary
                        |--> [hold queue] --> [case tool] --> [analyst]
```

## STRIDE per trust boundary

| Boundary | S | T | R | I | D | E | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| intake → VerifyChain (vendor trust boundary) | mutual TLS, key rotation | signed responses / response-id echo | vendor response id logged (REQ-004) | **PII in transit and at vendor** — minimum fields, encrypted transport, response retention terms | vendor outage → hold queue (REQ-003); quota alarms | vendor has zero authority over release — scores only | | REQ-003/004 |
| intake → hold queue | svc identity | idempotent enqueue | queue offsets | Confidential payloads encrypted at rest | depth alarms (REQ-102) | n/a | | |
| case tool → analyst | RBAC | disposition immutable | analyst action log | role views | n/a | analyst-only release of candidates | | REQ-002/004 |

## AI-specific threats

Not applicable — no LLM in this flow (vendor scoring is the vendor's model; its
outputs are scores routed to humans, never auto-dispositioned).

## Assumptions & accepted risks

| # | Assumption / accepted risk | Owner | Expiry |
| --- | --- | --- | --- |
| 1 | Vendor list coverage ≥ current licensed lists | FinCrime ops | contract review |
