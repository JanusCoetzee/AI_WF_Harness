# Runbook — <service name>

Live documentation: every incident that finds this wrong fixes it in the same PR as
the remediation.

## Service facts

| Field | Value |
| --- | --- |
| Purpose (one line) | |
| Tier / criticality | |
| Owners / escalation | primary: ___ secondary: ___ risk partner: ___ |
| Dashboards | |
| Logs / traces | |
| Dependencies (up/downstream) | |
| Pinned LLM model + prompt versions (if AI) | |

## Start / stop / restart

```bash
# exact commands, environment by environment
```

## Health interpretation

| Signal | Healthy looks like | Degraded means | First action |
| --- | --- | --- | --- |

## Alert catalog

Every alert has a next action; an alert without one gets deleted.

| Alert | Symptom users feel | Likely causes | Runbook action |
| --- | --- | --- | --- |

## AI-feature operations (delete if N/A)

| Situation | Action |
| --- | --- |
| Output schema-failure rate above ___ | Halt feature flag ___; fall back to ___ |
| Provider outage / latency spike | Fallback path: ___ |
| Suspected prompt injection in the wild | Capture sample → adversarial dataset; assess blast radius via tool allowlist |
| Cost anomaly (denial of wallet) | Quota check; per-caller breakdown at ___ |
| Model deprecation notice | Re-enter workflow at Stage 04 and run the Model & prompt upgrade protocol (EVAL-SPEC template): pin candidate, side-by-side evals, shadow + agreement rate, pre-decided deadline rule, cost re-baseline, HIL comms, inventory update, staged cutover, G5 |

## Known failure modes

| Failure | Detection | Remediation | Incident refs |
| --- | --- | --- | --- |

## Rollback

Exact, rehearsed procedure. Last rehearsal date: ______
