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

## Lanes — the two defined pressure valves

Deterministic controls need defined pressure valves or people route around them.
Both lanes leave a full audit trail; neither weakens a gate.

| Lane | For | How it works |
| --- | --- | --- |
| **Maintenance** (`/harness-maintain`) | Routine hygiene: dependency bumps, config rot, cert renewals | One `MAINT-YYYY-MM` batch dossier (`templates/MAINTENANCE.md`), one GC. Changelog review + green verify + clean audit stands in for per-package recon. **Ejection rules**: majors, verify failures, and auth/crypto/session/payment libraries always get an individual change — ejection is the lane working. |
| **Break-glass** (`/harness-breakglass`, gate **GE**) | Emergencies only: exploit in the wild, active customer harm, hard external deadline | Invoked by a **named human with authority**, never the AI. Part A record kept live as you act (timeline, interim mitigation, peer eyes, disclosed verify degradation, DECISIONS.log at deploy). Part B retrospective dossier within **2 business days**, retro on every use. A defined emergency path is what makes "no gate skipping" enforceable the rest of the time. |

## Directory map

```text
AI_WF_Harness/
├── CLAUDE.md              ← drop into your project; governs how the LLM behaves
├── harness.config.yaml    ← risk tiers, verify commands, gate policy
├── docs/
│   ├── PHILOSOPHY.md      ← why the harness works the way it does
│   ├── OPERATING-MODEL.md ← roles, segregation of duties, audit posture
│   └── harness/
│       └── OPERATING-PROTOCOL.md ← CLAUDE.md's companion: the "how" mechanics
│                            (session start, verify commands, milestone/traceability
│                            mechanics, slash-command reference) the constitution
│                            points to instead of duplicating
├── stages/                ← one playbook per stage (00-ideation … 08-operate,
│                            B0-change-intake + B1-reconnaissance for brownfield)
├── gates/GATES.md         ← entry/exit criteria + evidence per gate
├── templates/             ← PRD, ADR, PLAN, THREAT-MODEL, EVAL-SPEC, …
├── evals/harness/         ← the harness's own eval suite: scenarios, frozen
│                            ground truths, scored runs, manifest, REPORT.md
├── tests/                 ← app tests + eval regression (rides the verify loop)
├── .github/workflows/     ← CI: same verify.sh as local + full-history gitleaks
├── .claude/
│   ├── settings.json      ← hooks: command guards, commit traceability,
│   │                        verify-before-stop, session state injection
│   └── skills/            ← /harness-* slash commands for each stage + lanes
└── scripts/
    ├── verify.sh          ← the verify loop (typecheck→lint→test→eval→build)
    ├── gate-check.sh      ← asserts a gate's evidence exists before passage
    ├── evidence-bundle.sh ← builds the audit bundle for a release
    ├── audit-decisions.sh ← cross-checks STATE.md/CHANGE.md claims against DECISIONS.log
    ├── data-scan.sh       ← verify-time secret/PII pattern scan (ADR-007)
    ├── req-trace.sh       ← full REQ-### traceability walk for G5 review
    └── hooks/bash-guard.sh← blocks destructive commands at the tool layer
```

## Self-evaluation (evals)

The harness eats its own eval philosophy: [`evals/harness/`](evals/harness/) holds
six FinServ scenarios (greenfield AI feature, brownfield rounding fix, model
upgrade, break-glass RCE, regulatory restatement, vendor integration), each with a
**ground truth frozen before any run** and a mechanical scorer. Runs are produced
strictly from what the templates/skills elicit; failed checks fix the **harness**,
never the run artifacts. Thirteen template/skill improvements came out of run-1
failures; all six scenarios now score SATISFACTORY (MUST 100%).

Reproducibility is code: `manifest.yaml` pins each scenario's accepted run,
`tests/test_harness_evals.py` re-scores everything on every verify run, and CI
holds the line on every push. New ground truths follow the **blind-run protocol**
in the evals README — strongest when the GT author isn't the run author.

## Harness browser (UI)

A small Flask app renders the whole harness — pipeline map, stages, gates,
templates, skills, config — as a browsable UI, scanning the repo live so edits
show up on refresh. JSON catalog at `/api/catalog`.

```bash
python3 -m venv .venv && .venv/bin/pip install -r app/requirements.txt
.venv/bin/python app/server.py     # → http://localhost:5050
```

## Doctrine API + MCP tools (#10, #11)

The same content the browser renders is also servable machine-to-machine,
at an explicit, integrity-checked version — no vendoring, no `latest`
(see [`ADR-002`](docs/harness/adr/ADR-002-central-doctrine-service.md)).

**HTTP API** (`#10`): `GET /api/doctrine/{version}/manifest` and
`GET /api/doctrine/{version}/file?path=...`, served by `app/server.py`
alongside the browser. Every response is sha256-verified against the
manifest; a mismatch is a 500, never the tampered content.

**MCP tools** (`#11`): four read-only tools —
`harness_get_template`, `harness_get_gate`, `harness_get_standard`,
`harness_search_doctrine` — over `streamable-http` only (no stdio: it has
no per-request identity, which fail-closed authz depends on). Runs as a
second process alongside the browser (`#31`: same container, see
[below](#try-it-run-the-container-yourself)).

```bash
.venv/bin/python app/mcp_server.py     # → http://127.0.0.1:5051/mcp
claude mcp add --transport http harness-doctrine http://127.0.0.1:5051/mcp
```

v1 identity is a stub (bearer-token presence = authenticated, no real
OIDC yet — see `docs/harness/changes/GH-8/THREAT-MODEL.md`'s delta
review); every tool response still carries `{version, path, sha256}`
provenance, and a denied or tampered item returns a tool error, never
content. **This is fine for the local pilot below** (nobody but you can
reach your own `localhost`) and not yet fine for a shared, network-reachable
deploy — see that section for why the line is drawn there.

## Try it: run the container yourself

One image, both the browser and the MCP endpoint, proven live under
`docker --read-only` (`#31`). This is the fastest way to see the harness
against your own repo without installing anything but Docker:

```bash
docker build -t harness-doctrine .
docker run --rm --read-only -p 5050:5050 -p 5051:5051 \
  -v /path/to/your/repo:/harness:ro -e HARNESS_ROOT=/harness harness-doctrine
```

- Browser: `http://localhost:5050`
- MCP: `claude mcp add --transport http harness-doctrine http://localhost:5051/mcp`
  (or point any MCP-capable client at the same URL)

**Scope of this pilot, on purpose:** run it on your own machine, pointed at
your own checkout — not on a shared host reachable by anyone else. The
identity check is a stub (any bearer token is treated as authenticated,
see above); that's an accepted, deliberate limitation for **local, one-person-
per-instance use**, not a statement that it's ready for a shared or
internet-reachable deployment. Real SSO is still required before this runs
anywhere a stub identity would matter (`docs/harness/changes/GH-8/
THREAT-MODEL.md`'s Assumption #1) — this pilot doesn't change that, it
sidesteps it by construction (nobody but you can reach your own `localhost`).

**Found something confusing, wrong, or worth knowing while you're poking at
it?** File a GitHub issue and tag it `pilot-feedback` — that's the actual
point of this: real usage surfaces things a design session doesn't. Rough
edges in the MCP tool responses, gaps in what the browser shows, confusing
error messages, anything — even "this felt fine" is useful signal if you
say what you were trying to do. **Include which version you ran** (ADR-013,
GH-33) — `docker inspect --format='{{json .Config.Labels}}' <image>` if
you pulled a published tag, or the running container's own
`/api/health`/doctrine-manifest `git_commit`/`skills[]` fields either
way — so retro can tell whether your feedback is about the current build
or something already fixed in a later one.

## Quickstart (adopting the harness in a project)

1. Copy `CLAUDE.md`, `docs/harness/OPERATING-PROTOCOL.md`, `.claude/`, `scripts/`, `harness.config.yaml`, `gates/`, `stages/`, `templates/`, and `docs/` (`PHILOSOPHY.md`, `OPERATING-MODEL.md`, `STANDARDS.md`) into your repo (or reference this repo as a submodule). `CLAUDE.md` is the constitution (durable *why*); `OPERATING-PROTOCOL.md` is its required companion (the *how* — commands, mechanics, slash-command reference) — copy both. `gates/`/`stages/`/`templates/` aren't optional: every skill's own header cites them by relative path (e.g. `harness-ideate`: "Playbook: `stages/00-ideation.md`. Template: `templates/IDEA.md`") — skip them and every skill breaks immediately in the fresh repo. (This is today's fallback: ADR-002's target end state serves doctrine centrally instead of vendoring it, but that service isn't live yet — see [`docs/harness/adr/ADR-002-central-doctrine-service.md`](docs/harness/adr/ADR-002-central-doctrine-service.md).)
2. Edit `harness.config.yaml`: set the project's default risk tier and wire the `verify` commands to your real toolchain.
3. Create `docs/harness/` in your repo — all working artifacts (PRD, ADRs, plans, gate evidence) live there, versioned with the code.
4. Start a session: `/harness-status` tells you (and the LLM) which stage you're in and what the next gate demands.
5. Work the stages. **New build:** `/harness-ideate` → `/harness-prd` → `/harness-adr` → `/harness-plan` → `/harness-issues` → `/harness-build` → `/harness-review` → `/harness-secure` → `/harness-release` → `/harness-retro`. **Change to existing code (most work):** `/harness-change` (repairing the inbound ticket first via `/harness-issues` if it's vague) → `/harness-recon` → `/harness-build` → same back half.

## Non-negotiables

1. **No gate skipping.** A stage's outputs don't exist until the gate's evidence exists in the repo.
2. **Traceability or it didn't happen.** Every requirement gets a `REQ-###` ID at G1 (or the ticket key / `CHG-###` on the fast path); every commit, test, and ADR references the IDs it serves.
3. **The ticket is the prompt.** Work is built from Jira/GitHub issues that meet the Definition of Ready (`templates/ISSUE.md`): self-contained vertical slices, correct at birth. A vague ticket gets repaired before any code is written.
   This repo holds itself to it: every commit references an issue (enforced by the commit-guard hook); `NO-TICKET: <reason>` is the logged exception, not the norm — see issue #1 for the retroactive audit record of the era before this discipline, closed by the Driver.
4. **The AI never approves its own work.** Human review is a gate condition, not a courtesy.
5. **Verify loop after every change.** Not at the end of the day — after every change.
6. **Nothing classified above `Internal` enters a prompt** without an approved data-handling exception (see `docs/OPERATING-MODEL.md`).
