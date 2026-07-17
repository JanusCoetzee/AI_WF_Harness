---
name: harness-maintain
description: Maintenance lane — batch routine dependency bumps and config hygiene into one MAINT-YYYY-MM dossier with a single GC, ejecting majors and sensitive-library changes to the standard fast path. Use for Dependabot/renovate queues, scheduled patching, and security bumps that are not emergencies.
---

# harness-maintain

Template: `templates/MAINTENANCE.md` → `docs/harness/changes/MAINT-YYYY-MM/CHANGE.md`.
One batch, one GC (`scripts/gate-check.sh GC MAINT-YYYY-MM`). Emergencies (exploit
in the wild, P1) are NOT this lane — that's `/harness-breakglass`.

1. **Gather the queue**: pending Dependabot/renovate PRs, `pip-audit`/`npm audit`
   findings, expiring STD-004 waivers, cert/config rot.
2. **Classify and eject.** Ride the batch: patch/minor with clean changelog review.
   Eject to an individual `/harness-change`: major versions; anything failing
   verify; auth/crypto/session/payment libraries (individual scrutiny even at
   patch level); any changelog showing behavior change in a path this repo uses.
   Ejecting is the lane working, not failing — say what was ejected and why.
3. **Changelog review is the recon.** For each rider, read the release notes for
   the version span (fetch current docs — don't trust memory for API changes);
   record the review in the scope table. This review plus green verify plus clean
   audit IS the per-package recon waiver.
4. Apply the batch, run `scripts/verify.sh --log`, run the dependency audit; fill
   the dossier including MAINT-YYYY-MM.1-.3 acceptance criteria.
5. `scripts/gate-check.sh GC MAINT-YYYY-MM`; state what sign-off the tier needs.
   Commits reference `MAINT-YYYY-MM`.
6. Downstream gates per tier as usual — but note in the reviewer pack that this is
   a maintenance batch: reviewers check the scope table and ejection honesty, not
   line-by-line diffs of lockfiles.
7. Suggest a cadence if none exists (monthly, plus ad-hoc when a High lands).
