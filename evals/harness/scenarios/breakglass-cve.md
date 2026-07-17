# Scenario: actively exploited RCE in triage-svc's JSON parser (break-glass)

*Continuation of the PayGuard world. Input arrives as a security bulletin, mid-Friday.*

## The inbound bulletin (verbatim)

> **SEC-ALERT-311** — 2026-07-17 14:05 UTC
> **CVE-2026-31337** (CVSS 9.8, unauthenticated RCE) in `fastjson2` 2.4.x < 2.4.10.
> Exploitation observed in the wild; added to the CISA KEV catalog this morning.
> Affected internally: **triage-svc** (pins 2.4.9), which parses payment-hub events
> including externally influenced remittance text. Patch 2.4.10 is available
> (patch-level, no API changes per release notes). Treat as emergency.
> — Security Operations

## Facts available at the time

- triage-svc deserializes hub events with fastjson2; remittance text originates
  from payment senders — an attacker-writable path to the vulnerable parser.
- Patch 2.4.10 is a drop-in patch bump; vendor PoC for the CVE is public.
- Full verify suite takes ~8 minutes; smoke suite 90 seconds; canary deploy slot
  available immediately.
- The bank's WAF/gateway team can deploy a payload-signature rule within ~15
  minutes as an interim shield while the patch ships.
- Authority: S. Vance (CISO delegate) reachable by secure call; a.khan (senior
  engineer, not the Driver) available as peer.
- Normal fast-path scheduling (review + G6 + change slot) would land Monday —
  three days of exposure to an actively exploited RCE.
- 2026-07-17 is a Friday; two business days for Part B lands Tuesday 2026-07-21.
