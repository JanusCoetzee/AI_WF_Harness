# Operating Model

Roles, duties, and audit posture for AI-assisted delivery in a regulated environment.

## Roles

| Role | Held by | Duties |
| --- | --- | --- |
| **Driver** | Human engineer (you) | Frames tasks, makes decisions, owns every artifact the AI drafts. Accountable for all output. |
| **Pair** | LLM (Claude) | Drafts, implements, critiques, researches, runs the verify loop. Proposes; never approves. |
| **Reviewer(s)** | Human peer(s) | Gate G5. Independent of the Driver. Count set by risk tier (T1 = 2, T2 = 1). |
| **Risk/Sec partner** | Human (security, compliance, or model-risk) | Consulted at G2 (threat model) and G6. For AI features, owns eval-threshold sign-off on T1. |
| **Release approver** | Human with change authority | Gate G7. May be the same person as a Reviewer only on T2 and below. |

## Segregation of duties matrix

| Action | AI may do | AI may draft, human executes | Human only |
| --- | --- | --- | --- |
| Write code, tests, docs | ✅ | | |
| Run verify loop, report results | ✅ | | |
| Self-critique / adversarial review | ✅ (input to G5, never satisfies it) | | |
| Commit to feature branch | ✅ (when instructed) | | |
| Merge to protected branch | | ✅ | |
| Approve a gate | | | ✅ |
| Tag release / deploy | | ✅ (scripts) | ✅ (trigger) |
| Grant data-handling exception | | | ✅ (Risk partner) |

## Data classification and prompts

Classification ladder: `Public < Internal < Confidential < Restricted`.

- Default ceiling for prompt content: **Internal** (configurable per project, never
  upward without a written exception from the Risk partner, logged in `DECISIONS.log`).
- Production data never enters prompts, fixtures, or logs. Synthetic data generators
  live in the test tree and are reviewed like code.
- Repo content goes only to the sanctioned AI toolchain. No pasting code into
  unsanctioned web tools.

## Audit posture

The audit question is always: *"Show me why this change was made, who approved it, and
what evidence existed at the time."* The harness answers structurally:

- **Why** → PRD (`REQ-###`) + ADRs, versioned with the code.
- **Who** → gate records in `DECISIONS.log` + PR approvals (human identities).
- **Evidence** → verify logs, eval scores, threat model, review record — snapshotted
  into `docs/harness/evidence/<release>/` by `scripts/evidence-bundle.sh` at G7.

### DECISIONS.log format

One line per event, append-only, committed:

```text
2026-07-16 | G3 passed | j.doe | PLAN-0042 ratified, 6 milestones
2026-07-17 | override  | j.doe | started M2 before M1 demo recorded; reason: env outage
```

## AI-specific model risk

For any feature where an LLM makes or influences a decision:

- **Eval spec is mandatory** (see `templates/EVAL-SPEC.md`) with thresholds agreed
  before build. Below-threshold = failed verify = no gate passage.
- **Pin model and prompt versions.** A model upgrade is a change: run the eval suite,
  record scores, and pass it through G5 like any other change.
- **Human-in-the-loop by tier:** T1 decisions influenced by an LLM require a human
  checkpoint in the *product* flow, not just the delivery flow.
- Keep prompts in version control next to their evals. Prompts edited in a dashboard
  are prompts you cannot audit.
