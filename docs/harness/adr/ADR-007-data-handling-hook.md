# ADR-007 — Add a real-time secret/data-classification hook, don't wait for G6

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-25 |
| Deciders | janus (Driver) |
| REQs served | N/A — harness process improvement, not tied to a work-item REQ/CHG |

## Context

`CLAUDE.md` §6 ("Data handling — hard limits") is the constitution's most
absolute language: "**Never** place data classified above `Internal`... into
prompts, code samples, test fixtures, or logs," and "if you find a hardcoded
secret, stop and flag it immediately — do not commit anything until
resolved." Reviewing hook coverage across the constitution
(prompted by the question "wouldn't principles be better enforced with
hooks?"), every other operationally-critical section already has some
mechanical backstop: §1/§2 via `session-start.sh`/`stop-verify-check.sh`, §5's
commit-message rule via `commit-guard.sh`, §7 partially via `bash-guard.sh`
and `gate-check.sh`'s reviewer check. §6 has none — it is enforced only at
**G6**, the secure gate, which by design runs after Build (G4) and Review
(G5). By the time G6 scans for it, a secret or PII fragment may already be
written to disk, committed, pushed, or — if it landed in a prompt rather than
a file — sent to a model API outside this repo's control entirely. "Stop and
flag immediately" cannot be satisfied by a check that runs stages later.

Sections §3, §4, §8, §9, and the ADR-requirement clause of §5 were also
reviewed and are not included as candidate hooks here: each depends on
judgment a regex/pattern match cannot make (is this decision "non-obvious"?
is this rounding mode correct? does this recon actually understand the
code?). They stay constitution-only. This ADR is scoped to §6 alone, per the
one-decision-per-ADR rule (ADR-003 gave `CLAUDE.md` §5 that rule).

## Options considered

### Option A — Real-time PreToolUse hook on Edit/Write (and relevant Bash) for secret/PII patterns

- Sketch: a new `scripts/hooks/data-guard.sh`, wired as a `PreToolUse` hook
  matching `Edit|Write` (content of the write) and extended into
  `bash-guard.sh`'s existing Bash matcher (for heredocs/`echo >`/`cat >`
  patterns). Deterministic regex set mirroring common secret-scanner
  signatures (AWS/GCP key prefixes, PEM headers, generic
  `api[_-]?key\s*[:=]\s*['"][A-Za-z0-9]{16,}`, SSN-shaped `\d{3}-\d{2}-\d{4}`,
  card-number-shaped sequences). Blocks (exit 2) with the same escape hatch
  pattern as `bash-guard.sh`/`commit-guard.sh`: a human can override, but the
  override is logged to `DECISIONS.log`, never silent.
- Pros: catches the violation at the only point that matches "stop and flag
  immediately" — before the write happens, not stages later; consistent with
  the precedent already set by `commit-guard.sh`/`bash-guard.sh`, so it's not
  a new category of tooling, just one more hook in the same family; closes
  the one section of the constitution that currently has strictly weaker
  enforcement than its own language demands.
- Cons: regex-based secret/PII detection has real false-positive and
  false-negative rates (a high-entropy test fixture string trips it; a
  cleverly-formatted real secret slips past); adds friction to every
  Edit/Write call, including the vast majority that touch nothing sensitive;
  another script to maintain as secret formats evolve (new cloud provider key
  shapes, etc.).
- Risks: false positives erode trust in the hook and get "worked around"
  reflexively (e.g., writing secrets in two Edit calls to dodge single-match
  regex) rather than triaged; false negatives create false confidence that §6
  is now "handled," when G6's gate-time scan remains the actual backstop for
  anything the hook misses.

### Option B — No new hook; keep enforcement at G6 only (status quo)

- Sketch: make no change. §6 continues to rely on human/AI discipline during
  work and the G6 secure-gate scan (`secure-gate-record.md`, STD-005) as the
  sole mechanical check.
- Pros: zero new maintenance surface; zero false-positive friction; G6's scan
  presumably uses a maintained secret-scanning tool rather than a hand-rolled
  regex set, so it may already be more accurate than what a hook could
  cheaply implement.
- Cons: directly contradicts §6's own "stop and flag immediately" language —
  gate-time-only enforcement is stages too late by construction; leaves the
  one section phrased as an absolute hard limit as the one section with the
  weakest mechanical backing.
- Risks: a real leak (secret or PII) sits in the repo/history or in prompt
  context from Build through Review before G6 ever looks — by which point
  "stop and flag immediately" has already failed, and remediation is a
  bigger job (history rewrite, credential rotation, incident process) than
  prevention would have been.

### Option C — Move the scan earlier but keep it at verify-time, not tool-time

- Sketch: add a secret/PII pattern scan as a new step inside
  `scripts/verify.sh` (alongside `audit-decisions.sh`), running on every
  verify invocation rather than on every individual Edit/Write call.
- Pros: catches violations before a gate, same maintenance shape as
  `audit-decisions.sh` (one script, plain grep/regex, no JSON stdin parsing
  per tool call); no added friction on every single edit, only at verify
  time, which the harness already requires after every meaningful change
  (`CLAUDE.md` §2).
- Cons: still not "immediately" — a secret can sit in a file across several
  edits before the next verify run; relies on the disciplined verify-after-
  every-change habit actually holding, whereas a tool-layer hook fires
  unconditionally.
- Risks: closer to Option A's protection than Option B's, but the gap between
  "written" and "verified" is exactly the gap that "stop and flag
  immediately" is meant to close.

## Decision

**Option C.** Human override of the AI recommendation (Option A): the Driver
noted this repo sits behind additional guardrails outside the harness itself
that already catch serious PII/secret violations, so tool-layer blocking on
every single Edit/Write is unnecessary belt-and-suspenders for this
environment — a verify-time scan is enough of a second net given what's
already covering the first line of defense. Implemented as
`scripts/data-scan.sh`, chained into the `lint` step of `harness.config.yaml`
`verify:` (alongside `audit-decisions.sh`), scanning git-tracked and untracked
non-ignored files for AWS key ids, PEM headers, hardcoded api_key/password
assignments, and SSN/card-number-shaped strings. Escape hatch: a
`# data-scan: allow` comment on the offending line, not a `DECISIONS.log`
override — lower-stakes than `bash-guard.sh`/`commit-guard.sh` overrides
because the external guardrails remain the actual backstop.

AI recommendation (for the record, not what was chosen): Option A, on the
strength of §6's own "immediately" language. Recorded per `CLAUDE.md` §5 —
the audit trail must show the human's own reasoning, not just the
recommendation.

## Consequences

**Easier:** §6 violations get caught before the gate rather than only at G6,
for near-zero added friction — no per-edit blocking, just one more chained
command in a step that already runs on every verify.

**Harder / new commitments:** a secret can still sit in a file across several
edits before the next verify run (the gap Option A would have closed and
Option C accepts); the pattern set needs upkeep as secret formats change.

**Tripwire to revisit this ADR:** if a real §6 violation is later found to
have slipped past both this scan and the external guardrails before reaching
G6, that's the signal to reopen this ADR and reconsider Option A — the
"additional guardrails" premise this decision rests on would have been shown
insufficient on its own.
