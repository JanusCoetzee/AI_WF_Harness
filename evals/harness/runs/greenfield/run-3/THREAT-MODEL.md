# Threat Model — PayGuard payment-exception triage

| Field | Value |
| --- | --- |
| Tier | T1 (full STRIDE) |
| Reviewed by | Risk/Sec partner — pending G2 sign-off (not yet assigned) |
| Date / Delta-reviewed at G6 | 2026-08-12 |

## System sketch

```text
[Payments hub] --Kafka topic--> [PayGuard consumer] --redact/mask (REQ-203)--> [LLM gateway]  <- trust boundary!
                                        |                                            |
                                        |<---------- classification + confidence ----+
                                        |
                                        v
                              [Ops case tool] <-- analyst confirms (REQ-002) --> [Analyst]
                                        |
                                        v
                          [Audit/reconciliation log] (REQ-004, control totals)
```

Trust boundaries: (1) Kafka topic → PayGuard consumer (internal, but PayGuard
is new code with new privileges on Confidential data), (2) PayGuard →
LLM gateway (internal-but-separate service, redaction is the boundary
control), (3) PayGuard → ops case tool (writes routing recommendations that
influence analyst action on sanctions-adjacent work).

## STRIDE per trust boundary

| Boundary | S(poofing) | T(ampering) | R(epudiation) | I(nfo disclosure) | D(oS) | E(levation) | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Kafka topic → PayGuard consumer | Low — internal topic, existing hub auth | Med — a compromised/misbehaving upstream could tamper with exception data before PayGuard sees it | Low — topic already has hub-level provenance | N/A at this hop | Med — topic flood could exceed REQ-101's latency bar | N/A | Consumer validates message shape before processing; REQ-102 fail-open prevents a DoS here from blocking analyst intake | REQ-101, REQ-102 |
| PayGuard → LLM gateway | Low — internal gateway, service-to-service auth already governed | Med — a prompt-injection payload embedded in remittance free-text could attempt to alter classification behavior | Med — need to log exactly what was sent (post-redaction) for audit | **High** — raw Confidential remittance text must never reach this boundary unredacted | Low — gateway is shared infra with its own limits | N/A | REQ-203 redaction is the primary control; output schema validation (ADR-002) rejects any non-conforming gateway response; prompt-injection resistance is an EVAL-SPEC.md threshold, not assumed | REQ-203, ADR-002, EVAL-SPEC.md |
| PayGuard → ops case tool | Low — internal, existing tool auth | Med — a wrong or manipulated routing recommendation could misroute a sanctions-adjacent case indirectly (REQ-003 excludes sanctions-hold directly, but a *misclassified* case could be mislabeled as non-sanctions and routed automatically) | Low — REQ-004 requires actor+timestamp on every routed case | Low — case tool already holds this classification level | Low | Low — PayGuard has write access only to routing-recommendation fields, not case resolution | REQ-002's mandatory analyst confirmation is the control for the misclassification risk above — no auto-resolution, ever | REQ-002, REQ-003, REQ-004 |

## AI-specific threats (mandatory — LLM in the flow)

| Threat | Applies? | Mitigation | Verified at G6? |
| --- | --- | --- | --- |
| Prompt injection via untrusted input (user text, retrieved docs, tool results) | Yes — remittance free-text is customer/counterparty-authored, effectively untrusted input to the classification prompt | Redaction (REQ-203) reduces surface but does not eliminate it (injection text can survive PII redaction); output is schema-validated (category enum + confidence, not free text) so even a successful injection can't produce unsafe *output*, only a wrong classification, which REQ-002's human confirmation catches | Pending — EVAL-SPEC.md injection-resistance threshold must be met before G4 |
| Sensitive data leakage into prompts / provider logs | Yes — remittance text routinely contains PII/account numbers | REQ-203 redaction/masking before any gateway call; data inventory (PRD.md) marks raw remittance text as never entering prompts | Pending G6 data-handling sweep |
| Unsafe output handling (exec, SQL/HTML interpolation, auto-actions) | No auto-actions — output is a routing *recommendation* only, schema-validated, never executed or interpolated | Output schema validation (ADR-002); REQ-002 keeps a human in the loop before any case moves | N/A — no execution path exists |
| Excessive agency (model can cause more than the feature needs) | Low — model can only produce a classification+confidence; it cannot resolve, close, or auto-route (REQ-002) a case | Scope of the gateway call is classification-only; no tool access granted to the model | N/A by design |
| Model/prompt drift degrading a control | Yes — classification accuracy or abstention behavior could drift silently | EVAL-SPEC.md regression policy: every prompt/model change gets a full eval run before ship; online sampling per the eval spec's regression policy | Pending — ongoing at operate stage |
| Denial of wallet (cost amplification) | Low-Med — volume is bounded (~1,100/day known), but a topic flood (see STRIDE row above) could amplify gateway calls | Per-caller rate limit at the gateway boundary matching expected volume with headroom; budget alarm | Pending G4 build |

## Control failure semantics

| Control | On failure: open / closed | Consequence accepted | Decided by |
| --- | --- | --- | --- |
| Classification service (LLM gateway call) | **Open** — falls through to today's fully-manual triage | No automation benefit that day; zero new risk introduced, since manual triage is the current baseline | ADR-001 (REQ-102) |
| REQ-203 redaction/masking step | **Closed** — if redaction cannot be confirmed to have run, the exception must NOT reach the LLM gateway; falls to manual triage instead | Same as above (manual triage), but this is a named exception to the "fail open" default above — redaction is a *data-protection* control, and REQ-102's fail-open explicitly does not extend to it | This ADR/threat model — flagged for explicit G2 sign-off since it's a deviation from REQ-102's general fail-open stance |
| Sanctions-hold exclusion (REQ-003) | **Closed** — if classification cannot confidently determine an exception is NOT sanctions-hold, it must be treated as if it is (routed to manual, never auto-routed) | Conservative bias toward manual handling for anything sanctions-adjacent, by design | IDEA.md risk tier proposal (T1 rationale) |

## Assumptions & accepted risks

| # | Assumption / accepted risk | Owner | Expiry / revisit date |
| --- | --- | --- | --- |
| 1 | Redaction (REQ-203) is assumed to remove all PII from remittance free-text; no redaction technique is 100% — residual leakage risk is accepted pending the G6 data-handling sweep's actual measured rate on the eval dataset | Head of Payment Operations (business owner) | Revisit at first G6 pass — becomes a hard blocker if measured residual leakage > 0% on the eval set |
| 2 | Prompt-injection resistance threshold (EVAL-SPEC.md) is not yet measured — accepted as an open risk until G4 eval run | Driver | Revisit before G4 |
| 3 | Risk/Sec partner review (required for T1) has not yet occurred — this threat model is Driver-drafted, not yet reviewed | Driver, pending Risk/Sec assignment | Must resolve before G2 approval — this IS the G2 blocker, not a footnote |
