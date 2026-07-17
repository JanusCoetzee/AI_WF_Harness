# Scenario: LCR reclassification with discovered misreporting (regulatory report)

*Tracked as GitHub issue #2. Fictional but representative. Brownfield fast path on
a reporting pipeline; front-half artifacts (CHANGE, RECON) are in scope.*

## The inbound ticket (verbatim)

> **REG-9034** — LCR instruction update: fintech partnership deposits
> Regulator's updated reporting instructions (RI-2026-07, published this week):
> deposits sourced via fintech partnership programs must be reported as
> "less stable retail" instead of "stable retail", **effective the 2026-10 reporting
> period**. Please update the liqreport feed. — Reporting owner: t.okafor
> (Regulatory Reporting), accountable signatory for the LCR return.

## System facts (discoverable during recon)

- `liqreport` (Python) classifies deposit balances monthly and produces the LCR
  return submitted via the regulator portal on business day 15.
- Classification rules live in `liqreport/rules/deposit_classes.py`; the fintech
  partnership flag exists on accounts (`partner_program_id`) at line 142 but is
  **not consulted** — those deposits currently fall through to "stable retail".
- During analysis it emerges this fall-through has ALSO been misclassifying
  **operational corporate accounts** with a partner flag for the last 5 quarters —
  the submitted returns for those periods understated outflows. Estimated impact:
  0.6–0.9 percentage points on the reported LCR ratio per quarter.
- Prior-period returns are archived with the exact rule-code version used.
- The regulator's instruction is effective by **reporting period**, not by deploy
  date: the 2026-09 period must still be produced under the old rules even if the
  code ships in August.
- Submission calendar: monthly, BD15; a resubmission process for prior periods
  exists in the portal and requires the accountable signatory.
- t.okafor owns the regulator relationship; engineering never contacts the
  regulator directly.
