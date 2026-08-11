# RECON — GH-12

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| `evidence_dir(id)` helper | scripts/gate-check.sh:31-38 | already used by G0/G1/G2; resolves `$H/changes/<id>` if id given, else flat `$H` |
| G3 case | scripts/gate-check.sh:100-104 | reads `$H/PLAN.md` directly, no `evidence_dir` call |
| G5 case | scripts/gate-check.sh:112-117 | reads `$H/review-record.md` directly |
| G6 case | scripts/gate-check.sh:119-126 | reads `$H/secure-gate-record.md` directly |
| G7 case | scripts/gate-check.sh:128-132 | reads `$H/evidence/*/` and `$H/RELEASE-CHECKLIST.md` directly |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| Humans running gate checks by hand | invoke `scripts/gate-check.sh <GATE> [id]`; currently only G0/G1/G2/GC accept the id | usage string at scripts/gate-check.sh:8-11 |
| CI (`.github/workflows/verify.yml`) | does not call gate-check.sh at all | read the workflow file — only `scripts/verify.sh` + gitleaks run in CI |
| `/harness-review`, `/harness-secure`, `/harness-release` skills | tell the human to run `gate-check.sh G5/G6/G7` at the end of their stage | grep of `.claude/skills/harness-{review,secure,release}/SKILL.md` |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| No-id invocation reads the flat `docs/harness/` path | current behavior for every gate | keep as the no-id fallback (GH-12.1) — some adopting repos may not use per-item change dirs |
| `evidence_dir()` signature `(id)` → path string | scripts/gate-check.sh:32 | reused as-is for G3/G5/G6/G7, no signature change |

## Test coverage reality

- No existing test exercises `gate-check.sh` (bash script, outside the `pytest`
  suite; only `bash -n` syntax-checked by the lint step). The false-PASS this
  change fixes was found by running the script directly, not by a red test.
- This change adds no new automated test (bash script, no test harness for it
  in this repo) — verification is manual re-run of all eight gate cases with
  and without an id, output pasted into the PR/commit per CLAUDE.md §2's
  "show the failure" rule when a step can't be machine-verified.

## Surprises / archaeology

`DECISIONS.log` (2026-07-25) already fixed exactly this class of bug for
G0/G1/G2 and explicitly scoped the fix to those three gates — the omission of
G3/G5/G6/G7 from that fix looks like an intentional scope cut at the time, not
an oversight that was never noticed. No record of why G3/G5/G6/G7 were left
out; treating it as unfinished follow-through rather than a deliberate
decision, since no rationale is logged.

## Go / No-go

- [x] Blast radius confirmed (single file, no CI dependency); [x] no consumer contract broken (no-id path kept identical)
- **Recommendation:** go
