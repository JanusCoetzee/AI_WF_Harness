"""GH-26: gate-check.sh's need_file() must not false-positive on a template
placeholder pattern (e.g. `CHG-###`) mentioned in legitimate backtick-quoted
prose, while still catching a genuinely unfilled template. Written because
this exact bug shipped once (CHG-001 retro, docs/RETROS/RETRO-2026-08-18.md)
and the only verification it got before GH-26 was manual and throwaway —
nothing would have caught a regression.

Runs scripts/gate-check.sh via subprocess against fixture dirs, same pattern
tests/test_harness_evals.py already uses for score.py.
"""
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
GATE_CHECK = ROOT / "scripts" / "gate-check.sh"

FILLED_WITH_PROSE_MENTION = """\
# CHANGE — GH-TEST real filled-in change

| Field | Value |
| --- | --- |
| Status | Ratified (GC) |
| Driver | janus |
| Risk tier | T3 |
| Recon | waived-trivial (test) |

## Intent

Traceability note: commits reference the change ID (`CHG-###` pattern) per CLAUDE.md §5.

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| GH-TEST.1 | real content here |

## Blast radius

real content

## Rollback note

real content

## Escalation triggers

| Trigger | Yes/No | If yes → |
| --- | --- | --- |
| New external interface? | No | G2 |

## GC sign-off

T3: Driver.
"""

GENUINELY_UNFILLED = """\
# CHANGE — CHG-### <title>

| Field | Value |
| --- | --- |
| Status | Draft |

## Acceptance criteria

| # | Given / When / Then |
| --- | --- |
| CHG-###.1 | |
"""


def _run_gc(tmp_path: Path, change_md: str, recon_md: str | None = "go\n") -> subprocess.CompletedProcess:
    harness_dir = tmp_path / "docs-harness"
    change_dir = harness_dir / "changes" / "GH-TEST"
    change_dir.mkdir(parents=True)
    (change_dir / "CHANGE.md").write_text(change_md, encoding="utf-8")
    if recon_md is not None:
        (change_dir / "RECON.md").write_text(recon_md, encoding="utf-8")
    env = {"HARNESS_DIR": str(harness_dir), "PATH": "/usr/bin:/bin:/usr/local/bin"}
    return subprocess.run(
        ["bash", str(GATE_CHECK), "GC", "GH-TEST"],
        capture_output=True, text=True, cwd=ROOT, env=env,
    )


def test_backtick_quoted_pattern_mention_is_not_a_false_positive(tmp_path):
    """GH-26.1"""
    proc = _run_gc(tmp_path, FILLED_WITH_PROSE_MENTION)
    assert "unfilled template" not in proc.stdout, proc.stdout
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_genuinely_unfilled_template_still_fails(tmp_path):
    """GH-26.2"""
    proc = _run_gc(tmp_path, GENUINELY_UNFILLED, recon_md=None)
    assert "unfilled template" in proc.stdout, proc.stdout
    assert proc.returncode == 1


@pytest.mark.parametrize("change_id", [
    "GH-6", "GH-12", "GH-13", "GH-15", "GH-17", "GH-19", "GH-20", "GH-21",
    "GH-25", "GH-26", "GH-27", "GH-28", "GH-29",
])
def test_real_dossiers_still_pass_gc(change_id):
    """GH-26.3 — zero regression across every real dossier in the repo."""
    proc = subprocess.run(
        ["bash", str(GATE_CHECK), "GC", change_id],
        capture_output=True, text=True, cwd=ROOT,
    )
    assert "evidence PRESENT" in proc.stdout, f"{change_id}:\n{proc.stdout}"
