# Engineering Standards Register

The single home for developer standards and rules. Three laws govern this register:

1. **A standard stated only in prose is a suggestion.** Every entry must name the
   tool that enforces it and the verify step or gate where failure blocks progress.
   If no tool can enforce it, it's marked `manual (G5)` honestly — reviewers own it.
2. **One statement, many enforcers.** The threshold is defined once here (and
   machine-readably in `harness.config.yaml` `standards:`); tool configs implement
   it per stack. When the threshold changes, this file and the config change in the
   same commit as the tool configs.
3. **Waivers expire.** Any exception is logged in `DECISIONS.log` with an expiry
   date and an owner. No evergreen waivers.

## The register

| ID | Standard | Threshold | Enforced by (per stack) | Blocks at |
| --- | --- | --- | --- | --- |
| STD-001 | Unit test coverage on changed lines | ≥ 80% | Java: JaCoCo (`mvn verify` rule) · Python: coverage.py `--fail-under` · Node: vitest/jest `--coverage` thresholds | verify `test` step → G4 |
| STD-002 | Mutation test score | ≥ 80% | Java: PIT (pitest) `mutationThreshold` · Python: mutmut + score check · Node: Stryker `thresholds.break` | verify `test` step (or nightly CI on T2/T3 — see note) → G4 |
| STD-003 | Cognitive complexity per function | ≤ 12 | Java: SonarQube rule / Checkstyle `CyclomaticComplexity`-family · Python: ruff `C901` / radon cc · Node: eslint-plugin-sonarjs `cognitive-complexity: [error, 12]` | verify `lint` step → G4 |
| STD-004 | Dependency vulnerabilities | No High or Critical (CVSS ≥ 7) in any shipped dependency | Java: OWASP dependency-check Maven plugin `failBuildOnCVSS 7` · Python: pip-audit · Node: `npm audit --audit-level=high` · repo-wide: Dependabot/SCA | verify `build` step + G6 audit |
| STD-005 | No secrets in code or history | zero findings | gitleaks/trufflehog in CI + pre-commit | G6 (and immediately, per CLAUDE.md §6) |
| STD-006 | LLM output validated at runtime | every AI boundary has a schema; no casting | schema presence checked in review; eval `schema_valid` scorer ≥ 99% | verify `eval` step → G4; manual (G5) |
| STD-007 | Public API changes are contract-first | schema/OpenAPI diff precedes implementation | manual (G5) + contract tests where present | G5 |

Add rows with the next STD-###. Deprecate by striking through with a dated note —
never delete, auditors read history.

## Notes on the sharp edges

- **STD-001 measures changed lines, not repo-wide average.** Repo-wide targets
  punish people who touch legacy code; changed-line coverage keeps the standard
  fair in brownfield work (see stage B1 — characterization tests count).
- **STD-002 (mutation) is expensive.** Run full mutation testing in CI nightly or
  on the PR's changed files only (PIT/Stryker both support incremental modes);
  a full-suite mutation run as a local verify step will get skipped by humans and
  LLMs alike, and a skipped standard is a dead standard.
- **STD-003 uses *cognitive* complexity where the tool offers it** (Sonar's metric),
  cyclomatic as fallback. The number 12 is the ceiling, not the target.
- **STD-004 severity gate is "fix or waive with expiry"** — the waiver text lives in
  the G6 record with the CVE ID, the reason it's unexploitable in context, and the
  revisit date.

## Where standards apply in the workflow

- **Authoring time:** CLAUDE.md obliges the LLM to treat STD thresholds as failing
  conditions while writing — not discover them at gate time.
- **Every change:** the verify loop runs the enforcing tools (`harness.config.yaml`
  wires them per repo).
- **G4:** verify log is gate evidence; below-threshold = no passage.
- **G5:** reviewers own the `manual` rows; the review record says so.
- **G6:** STD-004/005 evidence is part of the secure-gate record.
- **Retro:** standards that produced no findings and no confidence, or that everyone
  waived, get challenged — this register is pruned like code.

## Institutional standards above this file

Bank-wide policies (approved patterns, crypto standards, data residency) outrank
this register. Where one applies, add a row that *references* it (`STD-### →
policy-id`) rather than paraphrasing it — paraphrases drift.
