# Scenario: PayGuard — payment-exception triage (greenfield)

*Input brief handed to the harness at Stage 00. Fictional but representative.*

A mid-tier retail bank's payment operations team (14 analysts) manually triages
~1,100 payment exceptions per day: format failures, sanctions near-miss holds,
insufficient-funds returns, suspected duplicates, and cutoff misses. Average handle
time is 6 minutes; SLA breaches are rising ~8% quarter on quarter, and two analysts
resigned citing workload. Ops leadership asks for "an AI thing that sorts the queue".

Known context the requester supplies when asked:

- Exceptions arrive on an internal Kafka topic from the payments hub; each carries
  payment reference, amount, currency, counterparty details, status codes, and
  free-text remittance information (which routinely contains customer names,
  account numbers, invoice details).
- Analysts currently work from a shared queue in the ops case tool; routing to the
  wrong specialist team is the biggest time-waster (~30% of cases bounce once).
- Sanctions-hold exceptions are subject to regulatory timelines; misrouting one has
  compliance consequences. Payment data is classified Confidential.
- The bank runs approved AWS accounts (EU region, data-residency constrained) and
  an approved internal LLM gateway; direct calls to public model APIs are banned.
- Sponsor: Head of Payment Operations. Budget appetite: one squad, one quarter.

The ask, restated: reduce misrouting and handle time by classifying and routing
exceptions automatically, with analysts staying accountable for outcomes.
