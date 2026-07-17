"""Eval regression: every scenario's accepted run must stay SATISFACTORY.

Runs score.py exactly as a human would (same CLI, same exit-code contract), so a
local pytest, the verify loop, and CI all reproduce the identical scoring path.
Issue #4.
"""
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = yaml.safe_load((ROOT / "evals" / "harness" / "manifest.yaml").read_text(encoding="utf-8"))
SCENARIOS = MANIFEST["scenarios"]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["name"] for s in SCENARIOS])
def test_scenario_stays_satisfactory(scenario):
    gt = ROOT / scenario["ground_truth"]
    run = ROOT / scenario["accepted_run"]
    assert gt.is_file(), f"ground truth missing: {gt}"
    assert run.is_dir(), f"accepted run missing: {run}"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "harness" / "score.py"), str(gt), str(run)],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, (
        f"{scenario['name']} dropped below SATISFACTORY:\n{proc.stdout}\n{proc.stderr}"
    )


def test_manifest_covers_all_ground_truths():
    """A ground truth without a manifest entry is a scenario silently excluded
    from regression — that's how coverage rots."""
    gt_dir = ROOT / "evals" / "harness" / "ground-truth"
    on_disk = {p.name for p in gt_dir.glob("*.yaml")}
    in_manifest = {Path(s["ground_truth"]).name for s in SCENARIOS}
    assert on_disk == in_manifest, (
        f"unpinned ground truths: {on_disk - in_manifest or 'none'}; "
        f"manifest entries without files: {in_manifest - on_disk or 'none'}"
    )
