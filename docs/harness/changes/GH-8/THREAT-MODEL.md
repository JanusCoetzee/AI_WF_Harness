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
| 6 | Version/deprecation drift across independent BU instances (ADR-008) is a human governance control, not a harness mechanism — the harness makes the manifest legible (provenance-stamped) but does not block, flag, or refuse a stale instance | janus | **Named trigger (GH-21):** revisit if *any* of — (a) a High/Critical-severity core or skill fix goes unpatched by any live BU instance more than 30 days after publish (mirrors STD-004's own High/Critical severity gate); (b) a 4th BU instance onboards (3 is small enough for a manual survey; 4+ makes "what is everyone running" genuinely unauditable by eye, per ADR-008's own "Harder" consequence); or (c) any incident traces to a stale instance running a since-fixed core/skill version. First trigger to fire wins — whichever comes first prompts the revisit, not all three |
| 7 | Shared artifact registry (`harness-core-vX.Y.Z`, `skill-NAME-vX.Y.Z`) is readable by every BU's build pipeline by default, same trust level as the original org-wide doctrine content — a BU publishing a skill containing BU-Confidential content to the shared namespace by mistake is a cross-BU leak this model does not itself prevent | janus | **Named trigger (GH-21):** revisit before a 3rd BU onboards (2 BUs sharing a namespace is a bilateral trust call the two Principal Engineers can make directly; 3+ needs an actual control), or immediately if #11 MCP's design has any skill read across BU boundaries (turns a publish-time risk into a runtime one), whichever comes first. **Obvious mitigation, propose now rather than later:** #10's manifest schema is still being finalized (STATE.md landmine: it must grow a `skills` array before that work locks) — add a required `classification` field per skill manifest entry (`Internal`/`Confidential+`), unlabeled or above-Internal defaulting to publish-blocked (same fail-closed pattern as risk/row 5's RBAC-at-retrieval default), enforced by the same publish-role + sha256-manifest mechanism ADR-008's registry boundary row already specifies. Cheaper to add to #10's in-progress schema now than to retrofit after BUs are already publishing unlabeled skills |

## Delta review — ADR-008 (2026-07-25): independent per-BU instances

ADR-008 supersedes the single-shared-service topology (rows above describing
"the service" now describe **one instance among N**, one per business unit).
The invariants carried forward unchanged: read-only service, content
integrity hash-pinned to signed tags, no write path, enforcement stays local.
What's new:

- **New trust boundary — shared artifact registry → per-BU build pipeline.**
  Core harness (`harness-core-vX.Y.Z`) and each skill/hook/workflow
  (`skill-NAME-vX.Y.Z`) are independently tagged and published once, then
  pulled by whichever BU instance's Principal Engineer chooses to compose
  them. This is the same shape as the existing CI→ECR→ECS boundary, applied
  one layer up the supply chain, and inherits the same mitigations
  (signed tags, sha256 manifest integrity, least-privilege publish role) —
  **provided those mitigations are explicitly extended to the skill tag
  namespace, not just the core namespace**, since skill content also enters
  LLM context and is therefore in-scope for the "flagship threat" (prompt
  injection via retrieved content) exactly like doctrine content is today.
- **Blast radius changed shape, not size.** A registry outage now blocks new
  *deploys/upgrades* across all BU instances, but — unlike the old single
  shared runtime service — does not affect any already-running instance
  (control failure semantics table's "Open — by design" row now applies at
  the registry layer too, for the same reason: enforcement and runtime
  availability never depend on the publish path).
- **New accepted risk, not yet mitigated:** rows 6–7 above. Neither is a
  STRIDE finding against a specific mechanism (there's no false claim of a
  control that isn't there); both are honest gaps this ADR chose to leave to
  governance and cross-BU trust respectively, recorded here so they're
  visible at G6 rather than rediscovered.

Full STRIDE table update (new registry boundary added):

| Boundary | S | T | R | I | D | E | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Shared registry → BU build pipeline | publish role scoped per namespace (core vs. skill) | tag tampering caught by same sha256-manifest integrity check as ADR-002 | publish events logged (extends CloudTrail coverage from CI→ECR) | skill content is in-scope for the Internal-max ceiling identically to doctrine — **not yet enforced for BU-authored skills specifically (risk #7)** | registry outage blocks new pulls only; running instances unaffected | only each namespace's designated publisher (core maintainers; the owning BU for their own skills) can publish to it | signed-tag verification extended to skill namespace; risk #7 open | ADR-002, ADR-008 |
