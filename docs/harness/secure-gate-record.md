# Secure Gate Record — CHG-001 (G6)

| Field | Value |
| --- | --- |
| Change | CHG-001 (commits 891e2c2, + G5 fix) |
| Tier | T2 — Driver walks checklist; no Risk/Sec partner required |
| Date | 2026-07-17 |

## 1. Secret scan — PASS (degraded, disclosed)

gitleaks/trufflehog not installed on this machine; ran pattern grep (API keys, AWS
key IDs, private key blocks, hardcoded credentials) over tracked files. **No
findings.** Degradation honestly noted: history-wide scan with a real tool is a
retro action before any T1 use of this repo.

## 2. Dependency audit — PASS

`pip-audit --local` over the venv (flask 3.1.3, markdown 3.10.2, pytest 9.1.1 and
transitive deps): **"No known vulnerabilities found."** STD-004 satisfied — no
High/Critical, no waivers needed.

## 3. Threat-model delta — PASS with note

No THREAT-MODEL.md exists (T2 fast path; GC accepted this). Delta review of what
was actually built:

- New surface: one read-only GET route, no parameters, no request body — returns
  counts already derivable from the pre-existing `/api/catalog`.
- Trust boundary unchanged: app binds 127.0.0.1:5050 (app/server.py:161); nothing
  is newly reachable.
- No new data flow, storage, or LLM touchpoint.
- **Note for the record:** if this app is ever bound beyond localhost, the entire
  catalog (internal process docs) becomes a data-exposure surface — that change
  would trip the escalation trigger to G2 and needs a real threat model.

## 4. Data-handling sweep — PASS

Grep of tests/, change artifacts, and evidence logs for realistic account numbers,
emails, credentials: no findings. Test data is counts of repo files only.

## 5. AI-feature checks — N/A

No LLM in the changed flow (the harness browser renders static documents).

## 6. Change record — SIMULATED

T2 requires a change-management ticket. Draft text prepared: "CHG-001: add
read-only health endpoint to internal harness browser; localhost-only; rollback =
revert + restart; evidence bundle attached." No real change system connected in
this drill — logged as a drill gap.

## Verdict

PASS at T2. Waivers: none needed.
