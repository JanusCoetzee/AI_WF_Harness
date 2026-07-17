# BREAK-GLASS — BG-### <one-line what>

Emergency path: act first, document as you act, full dossier within the deadline.
**Part A is filled at the moment of action — minutes, not hours. Part B is due
within 2 business days, and every use of this template triggers a retro.**

---

## Part A — at the time (complete before or during the fix, never after the fact)

### Timeline (append rows as you act — this table IS the proof of act-time documentation)

| Time (UTC) | Event |
| --- | --- |
| | alert/trigger received |
| | authorizing human contacted / authorization given |
| | this record opened |
| | interim mitigation requested / active (see below) |
| | fix built |
| | verification run (note degradation) |
| | peer eyes on diff |
| | deploy (canary / full) + DECISIONS.log written |
| | post-deploy checks |

A timeline reconstructed afterward has gaps and round numbers; one kept live has
neither. Auditors know the difference.

| Field | Value |
| --- | --- |
| Trigger | <CVE-####-#####, P1 incident id, regulator instruction — with link> |
| Why the normal path is too slow | <exploit in the wild / active customer harm / hard external deadline — be specific> |
| **Immediate mitigation while fixing** | <what shrinks exposure in minutes, before the fix ships: WAF/gateway rule, feature flag off, rate limit, isolation — or explicitly "none available" with why> |
| Comms during (not after) | <security ops / incident channel / change management notified — who, when> |
| Authorizing human (named, contacted how) | <break-glass is invoked by a human with authority; never self-invoked by the AI> |
| Peer eyes (named) | <second human who saw the diff before deploy — four eyes survives even here> |
| Scope of fix | <smallest change that removes the danger — no opportunistic extras> |
| Verify evidence | <full verify if possible; if degraded (subset of tests, no staging soak), say exactly what was skipped and why> |
| Rollback | <how, tested when> |
| Deployed | <time, by whom, where> |
| DECISIONS.log | `<date> | BREAK-GLASS | <authorizer> | BG-### <trigger>` — written at deploy time |

Rules that survive even in an emergency: secrets from vault only; no production
data into prompts; the AI drafts and verifies but a human triggers the deploy.

---

## Part B — retrospective dossier (deadline: 2 business days after Part A)

- [ ] CHANGE-equivalent: intent, blast radius, tier as it should have been
- [ ] RECON-equivalent: what the fix actually touched; consumers checked after the fact
- [ ] Full verify green (undegraded) on the shipped state
- [ ] Retrospective G5: independent human review of the emergency diff
- [ ] Retrospective G6: secret scan, dependency audit, threat-model delta
- [ ] **Compromise assessment** — if exploitation predated the alert, patching is
      not enough: logs searched for indicators of compromise over the exposure
      window; result recorded (clean / findings → incident process)
- [ ] Change record raised retroactively in the institutional system
- [ ] **Retro held** with the standing question: *was break-glass justified, and if
      the normal path was too slow for a legitimate change — what gets fixed in the
      path?* An unjustified use is an incident; a justified one that recurs is a
      process defect.

| Retro outcome | |
| --- | --- |
| Justified? | yes / no — reasoning |
| Path fix action (if the normal path was the problem) | action + owner + date |
