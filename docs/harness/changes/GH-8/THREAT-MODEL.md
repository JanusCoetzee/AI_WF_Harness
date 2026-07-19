# Threat Model — #8 Central harness doctrine service (ECS: browser + MCP)

| Field | Value |
| --- | --- |
| Tier | T2 (boundary table only) |
| Reviewed by | janus (Driver) — G2 pending |
| Date / Delta-reviewed at G6 | 2026-07-19 / pending |

## System sketch

```text
[Engineer browser] --https/SSO--> [internal ALB] --> [ECS task: browser UI]
[IDE MCP client]   --https/SSO--> [internal ALB] --> [ECS task: MCP endpoint]
                                                        |
                                     [content store <- signed git tag harness-vX.Y]
[GitHub Actions] --build/push--> [ECR image] --> [ECS task]
(later slice) [harvester] --read-only--> [team repos] --> [derived index]
```

Trust boundaries: (1) engineer→ALB, (2) IDE→ALB — **served content enters LLM
context**, (3) git tag→content store, (4) CI→ECR→ECS supply chain,
(5) harvester→team repos (deferred slice; delta-review when built).

## STRIDE per trust boundary

| Boundary | S | T | R | I | D | E | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Engineer → ALB → browser | SSO identity | TLS | ALB access logs | content is Internal-max; SSO required; internal subnets only | ALB + ECS autoscale; static content | no write routes exist (ADR-001) | SSO fail-closed; private subnets | ADR-001, ADR-002 |
| IDE → ALB → MCP | SSO/service token per team | **content hash-checked against signed tag manifest; mismatch = 500, never content** | provenance (`version`,`path`,`sha256`) in every response | same Internal ceiling; no team code flows *into* the service | read-only, cacheable; per-client rate limit at ALB | tools are read-only; no write tools without superseding ADR-002 | fail-closed integrity check | ADR-002 contracts |
| Git tag → content store | commits SSH-signed (issue #7) | tag built from signed commits; manifest sha256 per file | DECISIONS.log + signed history | n/a (public-to-org doctrine) | n/a | only CI can publish a version | signed-tag verification in build | ADR-002 |
| CI → ECR → ECS | GitHub OIDC role, no long-lived keys | image digest pinning in task def | ECR immutable tags + CloudTrail | n/a | n/a | task role = read-only; **read-only root filesystem** | least-privilege task role | ADR-002 |

## AI-specific threats (MCP content enters LLM context)

| Threat | Applies? | Mitigation | Verified at G6? |
| --- | --- | --- | --- |
| Prompt injection via retrieved docs | **Yes — the flagship threat.** A compromised service would inject instructions into every team's IDE sessions simultaneously. | Content integrity is fail-closed: served bytes must hash-match the manifest of a signed git tag; doctrine repo commits are signed; service filesystem read-only; clients pin `doctrine_version`. | pending |
| Sensitive data leakage into prompts/logs | Low — service holds doctrine only (Internal-max); no team code or data flows in. MCP *queries* could leak fragments → query logging redacted, `Internal` ceiling applies to logs. | Data inventory ceiling; no request-body persistence | pending |
| Unsafe output handling | Low — content is documentation rendered/read, never executed. Clients must still treat it as data, not instructions (standard demarcation). | Provenance headers; client-side demarcation | pending |
| Excessive agency | No — all MCP tools read-only by contract (ADR-002). | Adding any write tool supersedes ADR-002 | pending |
| Model/prompt drift degrading a control | Indirect — doctrine version drift. | Explicit version pin; no "latest" endpoint exists | pending |
| Denial of wallet | No — service makes no LLM calls. | n/a | — |

## Control failure semantics

| Control | On failure: open / closed | Consequence accepted | Decided by |
| --- | --- | --- | --- |
| SSO/auth at ALB | Closed — no anonymous access, service unreachable | Teams lose doctrine reads until auth restored | janus |
| Content integrity check (sha256 vs manifest) | Closed — 500, never serve unverified content | Availability sacrificed for integrity; alarm on mismatch | janus |
| Service availability for IDE sessions | **Open — by design.** Enforcement never depends on the service; sessions degrade to the vendored local minimum and gates remain enforceable | Sessions may use slightly stale doctrine while service is down | janus |
| Harvester repo access (later slice) | Closed — skip repo, mark dashboard stale, alert | Dashboard staleness; never fabricated data | janus |

## Assumptions & accepted risks

| # | Assumption / accepted risk | Owner | Expiry / revisit date |
| --- | --- | --- | --- |
| 1 | Org SSO (or equivalent internal auth) exists in front of the ALB | janus | before first deploy (G7 of build slice) |
| 2 | Single AWS account, internal subnets; no public exposure | janus | revisit if a second org/account adopts |
| 3 | Doctrine signing key has no passphrase (carried from issue #7) | janus | revisit at T1 use of the harness |
| 4 | Harvester boundary is modeled but deferred; full delta review before that slice ships | janus | at harvester slice G2/G6 |
| 5 | RBAC enforced at retrieval boundary only (ADR-002 amendment): service filters by SSO role claims before content enters LLM context; unlabeled content = most restrictive (fail-closed). v1 policy: all-authenticated-read-all while doctrine is Internal-org | janus | before any Confidential+ content is served |
