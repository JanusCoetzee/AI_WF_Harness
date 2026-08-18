# Secure Gate Record — #11 (G6)

| Field | Value |
| --- | --- |
| Change | #11 — MCP tools (M2), commit `357ae91` (build) + `6c3a46a` (CI fix) |
| Tier | T2 — Driver walks checklist; no Risk/Sec partner required |
| Date | 2026-08-18 |

## 1. Secret scan — PASS, same disclosed residual as #10, nothing new

- **Push-scoped (HEAD only, matches the real CI trigger shape)**:
  `gitleaks detect --source . --log-opts="-1"` — 1 commit scanned, **no
  leaks found**.
- **Full-history** (`gitleaks detect --source .`, no log-opts limit, 47
  commits): still surfaces the same 2 already-confirmed false positives
  `#10`'s G6 record investigated and disclosed — the fake-shaped demo
  token in `docs/harness/PLAN.md:127` (fixed forward to a placeholder
  shape, `6c3a46a`) and the `generic-api-key` false match on
  "unlabeled/unrecognized" prose in `docs/harness/changes/GH-10/
  review-record.md:55`. **No new finding from `#11`'s own commits.** Not a
  blocker for the same reason `#10`'s wasn't: the actual CI gate
  (push-scoped) is clean, both residuals were verified not to be secrets
  before any suppression, and rewriting already-pushed `main` history is
  the Driver's call, not something to do unasked to make a report look
  cleaner.

## 2. Dependency audit — PASS

`.venv/bin/python3 -m pip_audit -r app/requirements.txt` (same
requirements file as `#10`, **`mcp==2.0.0` new for `#11`**): **"No known
vulnerabilities found."** STD-004 satisfied — no High/Critical, no waivers
needed.

Note for whoever runs the next G6 in this repo: `.venv/bin/pip-audit`'s
own console-script shebang is stale (embeds an old volume-mount path from
when the venv was created, `/Volumes/Mac_Extended 1/...` vs the repo's
current mount) and fails outright — worked around by invoking the module
directly (`python3 -m pip_audit`) instead of the broken entry-point
script. Not a `#11`-scoped finding (pip-audit isn't wired into
`verify.sh`/CI, only ever run manually at G6, so this never silently
degraded any automated check) — but worth fixing the venv itself
(`pip install --force-reinstall --no-deps pip-audit`) before it trips up
a future session that doesn't know the workaround.

## 3. Threat-model delta — PASS

Full delta appended to `docs/harness/changes/GH-8/THREAT-MODEL.md`
("Delta review — #11"), not summarized-and-lost here. Highlights:

- Closes the two rows `#10`'s own delta explicitly left `N/A` pending
  `#11`: **Excessive agency** (all four tools verified read-only by a
  mechanical test, `test_11_3_no_write_tool_exists`, not just code
  review) and **sensitive data leakage via query/search**
  (`harness_search_doctrine` filters denied items out of the result set
  entirely, fail-closed, tested).
- Flagship threat (prompt injection via retrieved docs): **verified** —
  `#11` calls `#10`'s already-verified `read_file_verified` directly, no
  parallel content path to re-audit.
- **New, not previously named:** `mcp==2.0.0`'s OAuth resource-server
  middleware is doing real security enforcement (`401` before any tool
  code runs) that this repo doesn't own or test directly — named in
  `#11`'s own G5 review record as its "area of least confidence," now
  also recorded in the threat model as a supply-chain trust dependency to
  re-check on every future dependency-audit cycle, not just today's.
- Assumption #1 (real SSO) restated again, not silently carried forward as
  satisfied: `StubTokenVerifier` is the same shape as `#10`'s header stub,
  same **G7 deployment blocker**, unchanged by `#11`.

## 4. Data-handling sweep — PASS

`scripts/data-scan.sh` (ADR-007, `verify.sh`'s own lint step) — clean.
Manual check on `#11`'s new content specifically: `tests/
test_mcp_doctrine.py`'s fixtures use only synthetic tokens
(`"some-bearer-token"`, empty/whitespace strings) and reuse `#10`'s
existing synthetic doctrine-content fixtures — no realistic account
numbers, emails, or credentials introduced. `#11` serves the same
Internal-max doctrine content `#10` already gates; no new data
classification.

## 5. AI-feature checks — PASS (this is the first slice where these are load-bearing, not N/A)

`#10`'s G6 record marked this section N/A (no MCP tools existed yet).
`#11` is the actual AI-facing surface ADR-002's original threat model was
written for — content served through these tools enters LLM context
directly.

- **Injection mitigations claimed by the threat model, verified**:
  fail-closed content integrity (`IntegrityError` → `ToolError`, never
  content) and explicit-version-only (no versionless route exists,
  structurally) both carry over from `#10` unchanged and were re-confirmed
  live at `#11`'s own G5 (unknown-version and unknown-item both return a
  clean `isError`, never a crash or partial content).
- **Output schema-validated, never executed/interpolated**: every tool
  returns a plain `dict`/`list[dict]` (`{path, version, sha256, content}`
  or `{path, title, excerpt}`) — the MCP SDK serializes these as tool
  results; nothing in `#11`'s code path executes or interpolates model
  output back into a prompt or command. Content is documentation text
  handed to the calling client as data, same demarcation `#10`'s routes
  already relied on.
- **Tool allowlists / least agency**: exactly four tools registered, all
  read-only, mechanically pinned by `test_11_3_exactly_four_tools_
  registered` and `test_11_3_no_write_tool_exists` — not just a design
  intent, a regression test that fails if a fifth or a write tool is ever
  added without updating this gate's evidence.
- **Eval evidence current for the pinned model+prompt**: N/A — `#11`
  serves static doctrine content over MCP tools, it does not itself call
  or wrap an LLM (no prompt, no model pin to evaluate). The eval suite's
  own scope (`evals/harness/`) tests the harness's *authoring* skills
  against ground truth, not this serving layer; no eval gap introduced by
  `#11`.

## 6. Change record — real ticket, not simulated

`#11` itself (GitHub issue) is the change-management record, same
convention `#10`'s G6 record established — no separate `CHG-###` needed.

## Findings outside this change's scope (reported, not fixed here)

- `.venv/bin/pip-audit`'s stale console-script shebang (§2 above) — repo
  housekeeping, not `#11`'s to fix under this gate.
- `#9`'s own G6/threat-model delta was never done (named in
  `THREAT-MODEL.md`'s header row since `#10`'s G6, still not backfilled) —
  carried forward, not `#11`'s scope to close.
- `scripts/req-trace.sh` still can't see bare `#NN` IDs — same landmine
  `#10`'s G5 first named, `#11`'s G5 reconfirmed it, still not filed as
  its own issue.

## Verdict

**PASS** at T2. No waivers needed — both disclosed residuals (the
full-history gitleaks findings; the stale pip-audit shebang) are
non-blocking housekeeping/already-investigated items, not policy
exceptions requiring `expiry_date`/`owner` under `harness.config.yaml`'s
waiver rules.

**Driver verdict:** **Approve** ([issue #11 comment](https://github.com/JanusCoetzee/AI_WF_Harness/issues/11#issuecomment-5323596253), via ADR-012), 2026-08-18T04:26:40Z.

**G6 PASSED.**
