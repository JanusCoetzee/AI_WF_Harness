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

## Enforcement architecture: hooks vs. skills vs. rules

The dividing rule for where a MUST lives:

> **Mechanically checkable → hook. Requires judgment → skill. Shapes default
> behavior → CLAUDE.md rule.** A MUST that only lives in prose is a suggestion.

| Layer | Nature | What lives there |
| --- | --- | --- |
| **Hooks** (`.claude/settings.json` → `scripts/hooks/`) | Deterministic; harness-executed; the model cannot skip them | Destructive-command blocking, commit traceability, verify-before-turn-end, session state injection |
| **Skills** (`.claude/skills/`) | Model-invoked playbooks | Judgment work: PRD drafting, design alternatives, adversarial review, recon, threat-model deltas |
| **CLAUDE.md rules** | Always-loaded instructions | Defaults and posture: schema-first, small steps, honesty about red runs |
| **Humans** | Gates | Approval, waivers, risk acceptance — never delegated to hooks or models |

### The hook set

| Hook | Event | Enforces |
| --- | --- | --- |
| `bash-guard.sh` | PreToolUse (Bash) | No destructive/history-rewriting commands; release actions stay human |
| `commit-guard.sh` | PreToolUse (Bash) | Every commit references a ticket / REQ-### / CHG-### — or an explicit `NO-TICKET: <reason>` line |
| `post-edit-flag.sh` + `stop-verify-check.sh` | PostToolUse (Edit/Write) + Stop | The turn cannot end with code changed since the last green verify — run `scripts/verify.sh` or declare via `declare-unverified.sh` |
| `session-start.sh` | SessionStart | STATE.md + recent decisions injected into context automatically |

### Escape hatches are auditable, never silent

Deterministic controls need pressure valves or they get disabled wholesale. Every
valve here leaves a mark: `NO-TICKET:` is greppable in history;
`declare-unverified.sh` writes to `DECISIONS.log` and G4 cannot pass while the
declaration stands. An escape hatch that leaves no trace is a bypass; these are
confessions.

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
