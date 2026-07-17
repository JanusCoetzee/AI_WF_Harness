# BREAK-GLASS — BG-001 Patch actively exploited RCE (fastjson2) in triage-svc

## Part A — at the time

### Timeline (kept live as events happened)

| Time (UTC) | Event |
| --- | --- |
| 14:05 | SEC-ALERT-311 received (CVE-2026-31337, KEV-listed) |
| 14:18 | S. Vance (CISO delegate) authorized break-glass by secure call |
| 14:21 | this record opened; timeline started |
| 14:25 | interim mitigation requested: WAF payload-signature rule (gateway team) |
| 14:29 | security ops + change management notified in the incident channel |
| 14:40 | WAF rule active — external exposure shrunk while patch in flight |
| 14:44 | fix built: fastjson2 2.4.9 → 2.4.10 lockfile bump |
| 14:48 | PoC reproduction: exploits 2.4.9 ✗ / fails vs 2.4.10 ✓; smoke green (full suite skipped pre-canary — noted) |
| 14:52 | peer a.khan reviewed diff |
| 15:04 | canary deploy |
| 15:12 | full deploy + DECISIONS.log entry written |
| 15:31 | full verify suite completed post-deploy, ALL GREEN |

| Field | Value |
| --- | --- |
| Trigger | SEC-ALERT-311: CVE-2026-31337, CVSS 9.8 unauthenticated RCE in fastjson2 < 2.4.10; exploitation observed in the wild (CISA KEV); triage-svc parses attacker-writable remittance text through the vulnerable parser |
| Why the normal path is too slow | Normal fast-path scheduling lands Monday — three days of exposure to an actively exploited RCE on a service fed by external senders |
| Immediate mitigation while fixing | WAF payload-signature rule requested 14:25, active 14:40 — exposure reduced 32 minutes before the patch deployed |
| Comms during (not after) | Security ops + change management notified in the incident channel 14:29; security bridge kept open through post-deploy checks |
| Authorizing human (named, contacted how) | S. Vance (CISO delegate), secure call 14:18 UTC — authorized break-glass verbally, confirmed in the security bridge |
| Peer eyes (named) | a.khan reviewed the diff at 14:52 UTC before deploy |
| Scope of fix | fastjson2 2.4.9 → 2.4.10, the smallest change that removes the danger — lockfile bump only, no opportunistic extras |
| Verify evidence | Degraded: full 8-minute suite **skipped** pre-canary (time); ran instead — public PoC reproduction: exploits 2.4.9 ✗, fails against 2.4.10 ✓; smoke suite green (90s). Full suite completed post-deploy 15:31 UTC, ALL GREEN |
| Rollback | Repin 2.4.9 + redeploy (rollback returns the vulnerability — only for functional breakage, paired with service isolation) |
| Deployed | Canary 15:04 UTC, full 15:12 UTC, by janus (human-triggered) |
| DECISIONS.log | `2026-07-17 | BREAK-GLASS | S.Vance | BG-001 CVE-2026-31337 triage-svc` — written 15:12 UTC at deploy |

## Part B — retrospective dossier (completed 2026-07-20, within deadline)

- [x] CHANGE-equivalent: intent, blast radius (triage-svc only; no API change per release notes, confirmed), tier T1 as it should have been
- [x] RECON-equivalent: parser usage traced — hub event deserialization only; no other fastjson2 call sites; consumers unaffected (recommendation schema unchanged)
- [x] Full verify green (undegraded) on the shipped state — re-run 2026-07-20
- [x] Retrospective G5: independent review by a.khan + one more reviewer (T1 count), no findings
- [x] Retrospective G6: secret scan clean; dependency audit clean — CVE-2026-31337 no longer present (STD-004 closure); threat-model delta: none (same boundaries)
- [x] Compromise assessment: gateway + triage-svc logs searched 2026-07-20 over the
      exposure window (2.4.9 deploy date → patch) for indicators of compromise —
      known PoC signatures, anomalous deserialization errors, unexpected egress:
      **clean**; result filed with security ops against SEC-ALERT-311
- [x] Change record raised retroactively: EM-CHG-4471
- [x] Retro held 2026-07-20

| Retro outcome | |
| --- | --- |
| Justified? | yes — actively exploited RCE on an externally fed parser; three days of exposure was not acceptable |
| Path fix action | none required for path speed — the trigger was genuinely emergent; break-glass existed for exactly this. Action: add fastjson2 to the maintenance lane's watch list so future patches ride monthly batches before they become emergencies (owner: janus, due 2026-07-31) |
