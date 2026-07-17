# Stage 02 — Architecture

**Purpose:** Make the significant decisions on purpose, with alternatives on record. Exit: **G2**.

## Inputs

`PRD.md` (G1 passed), platform standards, existing estate constraints.

## LLM role

- **Design it twice.** For each significant interface or component shape, produce 2–3
  genuinely different designs (not one design and two strawmen), with trade-offs. The
  `/design-an-interface` skill automates this.
- Draft ADRs from `templates/ADR.md` for every significant decision — options
  considered, decision, consequences, REQs served.
- Define the **type/schema contracts first**: API shapes, message formats, and — for
  AI features — the runtime-validated schema of every LLM output.
- Draft the threat model (`templates/THREAT-MODEL.md`): STRIDE per trust boundary.
  For AI features add: prompt injection, output-handling, data leakage via prompts,
  excessive agency (what can the model *cause* if it goes wrong?).
- Draft `EVAL-SPEC.md` for each AI behavior: dataset, scorers, thresholds. Thresholds
  are agreed here, **before** anyone falls in love with a prompt.
- **Third parties are risk decisions, not implementation details.** Any external
  provider in a flow gets the PRD's Third-parties table (data shared + agreements,
  TPRM before build spend, contract gating production coupling, failure semantics,
  exit plan) and appears as a trust boundary here — with its control-failure
  semantics (fail-open/fail-closed) decided and named, never left emergent.

## Human role

- Choose between the presented designs; the ADR records why.
- Bring the Risk/Sec partner in *now* (T1), not at G6 when redesign is expensive.
- Validate fit with the institution's estate: approved patterns, network zones,
  data-residency, vendor/model approvals.

## Outputs

- `docs/harness/adr/ADR-###.md` (one per decision), `THREAT-MODEL.md`,
  `EVAL-SPEC.md` (if AI features).

## Anti-patterns

- ADRs written after the code, as fiction. Write them when the decision is live.
- A threat model that models the happy architecture instead of the deployed one.
- "We'll define eval thresholds once we see how it performs" — that's how thresholds
  become descriptions of whatever you shipped.
