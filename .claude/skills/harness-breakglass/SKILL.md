---
name: harness-breakglass
description: Emergency break-glass path — act-first documentation for critical CVEs being exploited, P1 incident hotfixes, or regulator-driven deadlines, with a mandatory retrospective dossier within 2 business days. Use ONLY when a named human with authority declares the normal path too slow.
---

# harness-breakglass

Template: `templates/BREAK-GLASS.md` → `docs/harness/changes/BG-###/BREAK-GLASS.md`.
Gate: **GE** (`gates/GATES.md`). This is a defined pressure valve, not a shortcut —
every use is logged at the moment of action and retro'd afterward.

Hard preconditions — refuse politely and route to the fast path if unmet:

- A **named human with authority** invokes it and is recorded as authorizer. You
  never invoke break-glass yourself, and "we're in a hurry" is not a trigger —
  exploit in the wild, active customer harm, or a hard external deadline is.
- A **second human** (peer eyes) will see the diff before deploy. Four eyes
  survives even here.

The sequence, in time order:

1. **Part A first, fix second — in parallel at worst.** Open the Part A record,
   start the **timeline table immediately**, and append rows as events happen —
   the live timeline is the proof this wasn't reconstructed afterward.
2. **Shrink exposure before the fix ships**: request the interim mitigation (WAF
   rule, flag off, rate limit, isolation) in the first minutes — it usually lands
   faster than the patch. Notify security ops / the incident channel *during*,
   not after. Then the **smallest fix that removes the danger** — no opportunistic
   extras; scope creep under adrenaline is how emergencies become outages.
3. **Verify as much as time allows** — full loop if possible; if degraded, record
   exactly what was skipped. Never zero verification: at minimum the failing case
   proven fixed and the smoke path green.
4. **Peer eyes on the diff**, then a **human triggers the deploy**. Rules that
   survive the emergency: secrets from vault only, no production data in prompts,
   AI drafts but never deploys.
5. **DECISIONS.log at deploy time**: `<date> | BREAK-GLASS | <authorizer> | BG-###`.
6. **Schedule Part B immediately** (deadline 2 business days): retrospective
   CHANGE/RECON, undegraded verify, retrospective G5 review and G6 scans, the
   **compromise assessment** (exploitation may predate the alert — search logs
   over the exposure window; patching alone proves nothing about the past),
   retroactive change record, and the retro with the standing question — was this
   justified, and if the normal path was too slow for legitimate work, what gets
   fixed in the path? Offer to create the tracking task before ending the session.
