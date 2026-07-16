# Scenario: stmtgen — interest rounding drift (brownfield)

*Input handed to the harness: one vague ticket plus a legacy system. Fictional but
representative; file paths below are scenario facts available to recon.*

## The inbound ticket (verbatim)

> **OPS-2214** — Statement totals wrong sometimes
> Interest line doesn't match ledger for some accounts. Pls fix asap - audit flagged.
> Reporter: b.naidoo (Ops Reconciliation)

## System facts (discoverable during recon)

- `stmtgen` is a Java 8 / Spring Boot 2.7 service, ~9 years old, generating monthly
  savings-account statements for ~2.1M customers.
- Interest accrual: `src/main/java/com/bank/stmtgen/accrual/AccrualAggregator.java`
  rounds each daily accrual line HALF_UP at line level (line 214), then sums.
- The core ledger accrues unrounded daily and rounds once at month-end using
  HALF_EVEN (banker's rounding) — the documented group accounting policy.
- Result: statement interest differs from ledger by −2 to +3 cents for ~0.4% of
  accounts each month. Ops writes off differences via a manual recon journal;
  internal audit has raised a finding (AUD-2026-041) about the recurring write-offs.
- Known consumers of the interest figure: customer PDF statements, the GL
  reconciliation export (`ReconExportJob.java`), and the annual tax-reporting feed
  (`TaxFeedBuilder.java`) which uses the *statement* figure, not the ledger figure.
- Statements for the current cycle generate on the 1st business day of each month;
  a change freeze applies for 2 business days around the run.
- Statement amounts are customer data, classified Confidential. Test environments
  hold masked data only.
- Team norm: `BigDecimal` with explicit `RoundingMode` everywhere; the HALF_UP at
  line level predates the current team and is undocumented.
