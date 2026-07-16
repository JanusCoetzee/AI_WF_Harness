#!/usr/bin/env python
"""Score a harness run against a frozen ground-truth checklist.

Usage: score.py <ground-truth.yaml> <run-dir>
Exit 0 if satisfactory (MUST 100%, SHOULD >= threshold), else 1.
"""
import re
import sys
from pathlib import Path

import yaml


def check_one(run: Path, check: dict) -> tuple[bool, str]:
    flags = 0 if check.get("case") else re.IGNORECASE
    pattern = re.compile(check["pattern"], flags | re.MULTILINE)
    matched_files = []
    for glob in check["artifact"].split("|"):
        matched_files.extend(sorted(run.glob(glob.strip())))
    if not matched_files:
        return False, f"artifact missing: {check['artifact']}"
    for f in matched_files:
        if pattern.search(f.read_text(encoding="utf-8")):
            return True, f.name
    return False, f"pattern not found in {[f.name for f in matched_files]}"


def main() -> int:
    gt_path, run_path = Path(sys.argv[1]), Path(sys.argv[2])
    gt = yaml.safe_load(gt_path.read_text(encoding="utf-8"))
    counts = {"MUST": [0, 0], "SHOULD": [0, 0]}  # [passed, total]

    print(f"scenario: {gt['scenario']}   run: {run_path.name}")
    print(f"{'id':7} {'lvl':6} {'ok':3} description")
    for check in gt["checks"]:
        ok, detail = check_one(run_path, check)
        counts[check["level"]][1] += 1
        counts[check["level"]][0] += ok
        mark = "✓" if ok else "✗"
        print(f"{check['id']:7} {check['level']:6} {mark:3} {check['desc']}")
        if not ok:
            print(f"{'':17}→ {detail}")

    must_p, must_t = counts["MUST"]
    should_p, should_t = counts["SHOULD"]
    must_pct = 100 * must_p / must_t if must_t else 100
    should_pct = 100 * should_p / should_t if should_t else 100
    th = gt["thresholds"]
    ok = must_pct >= th["must_pct"] and should_pct >= th["should_pct"]
    print(f"\nMUST {must_p}/{must_t} ({must_pct:.0f}%)  "
          f"SHOULD {should_p}/{should_t} ({should_pct:.0f}%)  "
          f"→ {'SATISFACTORY' if ok else 'NOT SATISFACTORY'} "
          f"(bar: MUST {th['must_pct']}%, SHOULD {th['should_pct']}%)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
