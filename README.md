# AI Workflow Harness

A drop-in operating system for building software **in partnership with an LLM**, from ideation to production deployment — hardened for a Principal engineer working inside a large financial institution.

## Design DNA

Two schools of thought, combined:

| Influence | What we took |
| --- | --- |
| **Matt Pocock** (type-safe, eval-driven engineering) | Schemas and types as guardrails, not prose. Spec-first. Tight verify loops (typecheck → lint → test → eval) that give the LLM fast, honest feedback. Evals as first-class tests for anything AI-powered. Small, independently verifiable steps. |
| **Tech With Tim** (pragmatic, momentum-driven building) | Milestone-driven delivery — every milestone ends *runnable and demoable*. Plan before code. Scaffold the structure first, then fill it in. Ship early, iterate visibly. |
| **FinServ hardening** (this harness's own contribution) | Risk tiers that scale ceremony. Stage gates with audit evidence. Traceability from requirement → commit → test. Segregation of duties: **the AI proposes, a human disposes**. Data-classification rules for what may enter a prompt. |

## The workflow at a glance

```text
 Greenfield / project-sized:
 IDEATE ──G0──▶ DISCOVER ──G1──▶ ARCHITECT ──G2──▶ PLAN ──G3──▶ BUILD
                                                                  │
   ◀──────────────────────────────────────────────────────────── G4
   │
 REVIEW ──G5──▶ SECURE ──G6──▶ RELEASE ──G7──▶ OPERATE ──▶ (retro feeds IDEATE)

 Brownfield fast path (most day-to-day work on existing code):
 CHANGE INTAKE ──▶ RECON ──GC──▶ BUILD ──G4──▶ (same pipeline as above)
        └─ escalation triggers exit to the full path at G1/G2 ─┘

 Lanes: MAINTENANCE (batch hygiene, one GC) · BREAK-GLASS (emergencies, gate GE:
 act-first with a 2-business-day retrospective dossier)
```

Each stage has: purpose, inputs, **LLM role**, **human role**, outputs, and an exit **gate** with evidence requirements. Gates are defined in [`gates/GATES.md`](gates/GATES.md). How much gate ceremony applies depends on the work item's **risk tier** (see `harness.config.yaml`).

## Directory map

```text
AI_WF_Harness/
├── CLAUDE.md              ← drop into your project; governs how the LLM behaves
├── harness.config.yaml    ← risk tiers, verify commands, gate policy
├── docs/
│   ├── PHILOSOPHY.md      ← why the harness works the way it does
│   └── OPERATING-MODEL.md ← roles, segregation of duties, audit posture
├── stages/                ← one playbook per stage (00-ideation … 08-operate,
│                            B0-change-intake + B1-reconnaissance for brownfield)
├── gates/GATES.md         ← entry/exit criteria + evidence per gate
├── templates/             ← PRD, ADR, PLAN, THREAT-MODEL, EVAL-SPEC, …
├── .claude/
│   ├── settings.json      ← hooks: command guards, commit traceability,
│   │                        verify-before-stop, session state injection
│   └── skills/            ← /harness-* slash commands for each stage
└── scripts/
    ├── verify.sh          ← the verify loop (typecheck→lint→test→eval→build)
    ├── gate-check.sh      ← asserts a gate's evidence exists before passage
    ├── evidence-bundle.sh ← builds the audit bundle for a release
    └── hooks/bash-guard.sh← blocks destructive commands at the tool layer
```

## Harness browser (UI)

A small Flask app renders the whole harness — pipeline map, stages, gates,
templates, skills, config — as a browsable UI, scanning the repo live so edits
show up on refresh. JSON catalog at `/api/catalog`.

```bash
python3 -m venv .venv && .venv/bin/pip install -r app/requirements.txt
.venv/bin/python app/server.py     # → http://localhost:5050
```

## Quickstart (adopting the harness in a project)

1. Copy `CLAUDE.md`, `.claude/`, `scripts/`, and `harness.config.yaml` into your repo (or reference this repo as a submodule).
2. Edit `harness.config.yaml`: set the project's default risk tier and wire the `verify` commands to your real toolchain.
3. Create `docs/harness/` in your repo — all working artifacts (PRD, ADRs, plans, gate evidence) live there, versioned with the code.
4. Start a session: `/harness-status` tells you (and the LLM) which stage you're in and what the next gate demands.
5. Work the stages. **New build:** `/harness-ideate` → `/harness-prd` → `/harness-adr` → `/harness-plan` → `/harness-issues` → `/harness-build` → `/harness-review` → `/harness-secure` → `/harness-release` → `/harness-retro`. **Change to existing code (most work):** `/harness-change` (repairing the inbound ticket first via `/harness-issues` if it's vague) → `/harness-recon` → `/harness-build` → same back half.

## Non-negotiables

1. **No gate skipping.** A stage's outputs don't exist until the gate's evidence exists in the repo.
2. **Traceability or it didn't happen.** Every requirement gets a `REQ-###` ID at G1 (or the ticket key / `CHG-###` on the fast path); every commit, test, and ADR references the IDs it serves.
3. **The ticket is the prompt.** Work is built from Jira/GitHub issues that meet the Definition of Ready (`templates/ISSUE.md`): self-contained vertical slices, correct at birth. A vague ticket gets repaired before any code is written.
4. **The AI never approves its own work.** Human review is a gate condition, not a courtesy.
5. **Verify loop after every change.** Not at the end of the day — after every change.
6. **Nothing classified above `Internal` enters a prompt** without an approved data-handling exception (see `docs/OPERATING-MODEL.md`).
