---
name: harness-adr
description: Stage 02 — design decisions with real alternatives (ADRs), threat model, and eval specs for AI features, targeting gate G2. Use for any significant architecture or interface decision.
---

# harness-adr

Playbook: `stages/02-architecture.md`. Templates: `ADR.md`, `THREAT-MODEL.md`,
`EVAL-SPEC.md`. Exit: G2.

Precondition: G1 in `DECISIONS.log` (T1/T2 with novel architecture).

1. For each significant decision, **design it twice**: produce 2–3 genuinely
   different options — different shapes, not one favorite plus strawmen. (For
   interface design, the `design-an-interface` skill parallelizes this.)
   Present the trade-offs compactly; the **human chooses**.
2. Write `docs/harness/adr/ADR-###.md` per decision: options, the discriminating
   reason, consequences, tripwire for revisiting, REQs served. If you recommended
   the winning option, say so in the ADR — the audit trail must show the human's
   own reasoning too.
3. Define **contracts first**: API/message schemas, and for every AI behavior the
   runtime-validated output schema (Zod/JSON Schema/pydantic to match the repo).
4. Draft the threat model per tier (full STRIDE for T1; boundary table for T2),
   including the AI-specific table: prompt injection, data leakage, unsafe output
   handling, excessive agency, drift, denial-of-wallet.
5. For each AI behavior, draft `EVAL-SPEC.md` with dataset plan, scorers, and
   **thresholds agreed now** — before anyone falls in love with a prompt.
6. Update `STATE.md`; state G2 needs: human approval, Risk/Sec partner on T1.
