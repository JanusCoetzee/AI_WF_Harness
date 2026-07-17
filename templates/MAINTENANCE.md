# MAINTENANCE — MAINT-YYYY-MM <cycle label>

Batch record for routine hygiene: dependency bumps, config rot, cert renewals.
One dossier per cycle, one GC, instead of ceremony theater per package.

| Field | Value |
| --- | --- |
| Status | Draft / **Ratified (GC)** / Done |
| Driver | |
| Date | |
| Risk tier | highest tier of any service this batch ships into — usually T2 |
| Linked records | CVE ids, Dependabot/renovate PRs, expiring waivers this closes |
| Timing constraints | freeze windows / cycles that gate the deploy |

## Lane rules (what may ride this batch)

- **In:** patch and minor bumps whose changelog/breaking-change review is clean and
  whose verify run is green; config hygiene with no behavior change.
- **Ejected to an individual fast-path change:** major versions; anything that
  fails verify; anything touching auth, crypto, session, or payment libraries
  (those earn individual scrutiny even at patch level); any bump whose changelog
  shows behavior change in a path we use.
- Per-package recon is **waived by this lane's rules** — the waiver is the batch's
  changelog review + green verify + clean audit, recorded below. An ejected item
  is not a failure; it's the lane working.

## Scope

| Package | From → To | Semver | Reason (CVE / hygiene) | Changelog reviewed | Verify |
| --- | --- | --- | --- | --- | --- |

## Acceptance criteria

| # | Given / When / Then |
| --- | --- | 
| MAINT-YYYY-MM.1 | Given the full batch applied, when `scripts/verify.sh` runs, then ALL GREEN |
| MAINT-YYYY-MM.2 | Given the batch, when the dependency audit runs, then no High/Critical remain (STD-004) and any closed waivers are noted |
| MAINT-YYYY-MM.3 | Given the scope table, when reviewed, then it contains no major bumps and no ejected-category packages |

## Blast radius

| Aspect | Assessment |
| --- | --- |
| Services shipping this batch | |
| Highest-tier consumer among them | <sets the batch's tier above> |
| Deploy surface | lockfile/manifest only (anything more doesn't belong here) |

## Rollback note

Revert the lockfile/manifest commit; no migrations, no config semantics changed
(anything that would break this claim doesn't belong in the batch).

## GC sign-off

Per tier (T2: Driver; T1: Driver + peer). DECISIONS.log:
`<date> | GC passed | <who> | MAINT-YYYY-MM (<n> bumps, <m> ejected)`
