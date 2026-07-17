# Scenario: real-time sanctions screening via vendor API (third-party integration)

*Tracked as GitHub issue #3. Greenfield front-half focus: PRD, THREAT-MODEL, ADR.*

The payments hub screens counterparties against sanctions lists in a nightly batch;
the business wants real-time screening at payment intake using **VerifyChain Ltd**,
a screening SaaS. Facts available when asked:

- The API takes counterparty name, address fragments, and bank identifiers —
  customer PII, classified Confidential — and returns match candidates with scores.
- VerifyChain: SOC 2 Type II report available; hosts in EU and US regions; the
  bank's third-party risk process (TPRM) issues a vendor risk assessment reference
  (VRA-####) after due diligence — **not yet started** for VerifyChain.
- Contract is in procurement negotiation; a vendor sandbox with synthetic list data
  is available today; production API keys only issue after contract signature.
- Screening is a **control**: a payment must never proceed unscreened. Vendor SLA
  on offer: 99.9%, p95 300ms.
- The incumbent nightly batch remains in place during any transition.
- Bank policy: customer data leaves the estate only under a signed data-processing
  agreement (DPA) with residency guarantees; exits from material vendors require a
  documented exit plan (data return/deletion, replacement path).
