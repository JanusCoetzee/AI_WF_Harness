# RECON — GH-26

## Code map

| What | Where (file:line) | Notes |
| --- | --- | --- |
| `need_file()` | `scripts/gate-check.sh:17-26` | called by every gate case (G0/G1/GC/etc.) that checks a templated doc exists and is filled in |
| The false-positive regex | `scripts/gate-check.sh:21` (pre-fix) | `grep -qE 'CHANGE_ME|<work item name>|<name>|CHG-###' "$f"` — bare substring match, no positional context |
| Template's own placeholder positions | `templates/CHANGE.md:1,28-29` | title line (`# CHANGE — CHG-### <title>`) and unfilled acceptance-criteria rows (`| CHG-###.1 | |`) — neither is backtick-wrapped in the raw template |
| Template's own prose mention | `templates/CHANGE.md:24` | `` Commits, tests, and the PR reference `CHG-###`. `` — backtick-wrapped, and confirmed (grep) this exact line does not survive into any real filled dossier (`docs/harness/changes/GH-25/CHANGE.md` has no `CHG-###` occurrence at all) |

## Consumers found

| Consumer | How it depends | Found via |
| --- | --- | --- |
| Every `/harness-*` skill that runs `gate-check.sh` at its exit gate | indirectly, via the script | grep of skill files' gate references |
| Humans running `gate-check.sh` by hand | directly | usage string, README |
| CI | not called from CI (`verify.yml` only runs `verify.sh` + gitleaks) | read the workflow file |

## Implicit contracts (Hyrum's law inventory)

| Observed behavior | Evidence | Safe to change? |
| --- | --- | --- |
| Bare (non-backtick) `CHG-###`/`CHANGE_ME`/`<work item name>`/`<name>` in a value position (title, empty table cell) means unfilled | confirmed by testing a raw `templates/CHANGE.md` copy through `gate-check.sh` | keep — this is the actual signal the check should be keying on |
| A backtick-quoted mention of the pattern in explanatory prose is not a placeholder | reproduced false positive directly (retro's exact scenario), confirmed the template's own line 24 uses the same style | change — this was the bug, now excluded before matching |

## Test coverage reality

- No existing automated test exercised `gate-check.sh` before this change
  (bash script, outside the `pytest` suite — same gap noted in GH-12's
  RECON.md). **Closed now**: `tests/test_gate_check.py` (15 cases) — the
  false-positive repro, the genuinely-unfilled-template true-positive, and a
  parametrized sweep of every real dossier in the repo, all via `subprocess`
  against `gate-check.sh` itself (same pattern `test_harness_evals.py`
  already uses for `score.py`). Confirmed red against the pre-fix script
  (stashed the fix, reran, watched it fail for the right reason) before
  restoring it. Wired into `verify.sh`'s `test` step permanently — a future
  regression of this fix now fails CI, not just a future manual re-check.
- Verified manually, live, before drafting the persisted test: (1) the exact
  reproduced false-positive case now passes, (2) a genuinely unfilled raw
  `templates/CHANGE.md` copy still correctly fails, (3) every real dossier
  under `docs/harness/changes/*/` re-checked — no new regressions (two
  pre-existing, unrelated failures confirmed unchanged: GH-8 has no
  `CHANGE.md` by design, GH-14 correctly still trips GH-18's separate
  escalation-trigger check).

## Surprises / archaeology

Process substitution (`<(...)`) silently broke `grep` in this environment
mid-testing — plain files and pipes work correctly. Not investigated further
(likely the `rtk` command-rewrite hook mishandling `/dev/fd/N` paths), but
the shipped fix uses a plain pipe (`sed ... | grep ...`), not process
substitution, so it isn't exposed to whatever that was.

## Go / No-go

- [x] Blast radius confirmed (single function, no CI dependency)
- [x] Both directions verified live (false positive gone, true positive kept) before drafting this dossier
- **Recommendation:** go
