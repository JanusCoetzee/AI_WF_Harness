# Threat Model — #8 Central harness doctrine service (ECS: browser + MCP)

| Field | Value |
| --- | --- |
| Tier | T2 (boundary table only) |
| Reviewed by | janus (Driver) — G2 pending |
| Date / Delta-reviewed at G6 | 2026-07-19 / #10 delta reviewed 2026-08-18 (below); #9's container slice still has no delta review of its own — named, not backfilled here |

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

## Delta review — #10 (2026-08-18): doctrine API + authz interface built, G6

`#10` implements the read-side of ADR-002's contracts against real code for
the first time (`#9` proved the container could serve content at all;
`#10` is the first slice where the mitigations below are actually load-
bearing, not just designed). Updating the AI-specific threats table's
"Verified at G6?" column for the rows `#10` actually delivers — the
original table is left as the record of what was designed at G2; this
delta is what got built and tested.

| Threat | Verified at G6 for `#10`? |
| --- | --- |
| Prompt injection via retrieved docs (flagship threat) | **Verified.** Fail-closed content integrity shipped and tested: `app/doctrine.py::read_file_verified` raises on a sha256 mismatch, `app/server.py` turns that into a 500 that never serves the mismatched bytes (`tests/test_doctrine_api.py::test_10_2_*`). No `latest` endpoint exists — every read is against an explicit, auditable version (`test_10_3_*`) |
| Sensitive data leakage into prompts/logs | N/A for `#10`'s actual surface — no query/search route exists yet (`harness_search_doctrine` is `#11`'s, out of scope here). Nothing `#10` added persists request bodies |
| Unsafe output handling | Unchanged — still a client-side demarcation concern, `#10` serves data, not instructions, same as before |
| Excessive agency | N/A for `#10` — no MCP tools exist yet (`#11`, still pending). `#10`'s two HTTP routes are both `GET`, no write path |
| Model/prompt drift degrading a control | **Verified.** Explicit-version-only is enforced in code, not just policy (`app/server.py` route table has no versionless/`latest` route at all — structurally absent, not merely rejected) |
| Denial of wallet | N/A — unchanged, no LLM calls in `#10`'s code path |

**RBAC-at-retrieval (STRIDE table's IDE→ALB→MCP row, ADR-002 amendment):**
`#10` is the first code that actually implements "the service filters
fail-closed" rather than describing it — `app/doctrine.py::is_allowed()`
denies on missing/unrecognized classification regardless of identity, and
the manifest route filters its own listing (not just gated fetches) by the
same function. Verified live during `#10`'s G5, not just by unit test
(unauthenticated request → empty `files[]`).

**Assumption #1 still open, flagged again rather than silently carried:**
real SSO/OIDC is explicitly out of scope for `#10` (its own ticket body) —
identity is a documented header stub (`X-Harness-Actor`), authenticated =
presence of any non-empty value, no verification of who's asserting it.
THREAT-MODEL.md's own assumption #1 ("Org SSO exists... before first
deploy, G7 of build slice") is not yet satisfied and must not be treated
as satisfied by `#10`'s stub — this is a **G7 blocker for actual
deployment**, not a `#10` gap, but worth restating here so it doesn't get
lost between now and whenever `#7` (deploy) is worked.

## Delta review — #11 (2026-08-18): MCP tools built, G5 passed, G6

`#11` is the MCP half of the `IDE → ALB → MCP` boundary the STRIDE table
already described at G2 — the first code exercising it. Closes the two
rows `#10`'s delta explicitly left N/A pending `#11`.

| Threat | Verified at G6 for `#11`? |
| --- | --- |
| Prompt injection via retrieved docs (flagship threat) | **Verified**, same mechanism as `#10` — `#11` calls `app/doctrine.py::read_file_verified` directly (no parallel content path), so fail-closed integrity and explicit-version-only both carry over unchanged, not re-implemented. Confirmed live at `#11`'s own G5 (`isError` on unknown version, no silent fallback) |
| Sensitive data leakage into prompts/logs | **Verified.** `harness_search_doctrine` is the query/search route `#10`'s delta named as `#11`'s to cover — `_search()` filters denied items out of the result set entirely (`continue`, not an error), tested (`tests/test_mcp_doctrine.py::test_11_4_search_silently_omits_denied_items_not_erroring`, `test_11_wrapper_search_doctrine_returns_empty_when_unauthenticated`). No request-body persistence added |
| Unsafe output handling | Unchanged — `#11` returns the same `{path, version, sha256, content}` shape as `#10`'s HTTP routes; still documentation data, not instructions, same client-side demarcation |
| Excessive agency | **Verified.** All four registered tools are read-only by construction — `tests/test_mcp_doctrine.py::test_11_3_exactly_four_tools_registered` and `test_11_3_no_write_tool_exists` pin this mechanically, not just by code review. Adding a fifth tool or any write tool still supersedes ADR-002, unchanged |
| Model/prompt drift degrading a control | Unchanged from `#10` — `_resolve_manifest_or_error` calls the same explicit-version-only `build_manifest`, no versionless path exists in `#11` either |
| Denial of wallet | N/A — unchanged, no LLM calls in `#11`'s code path either |

**New trust dependency, not previously named:** `#11` is the first code in
this repo where a third-party library (`mcp==2.0.0`'s OAuth resource-server
middleware) does real security enforcement this repo doesn't own or test
directly — the 401-before-any-tool-code-runs behavior confirmed live at G5
depends partly on the SDK's own correctness, not only `app/mcp_server.py`'s
(`#11`'s review record names this as its "area of least confidence,"
repeated here since threat-model coverage, not just a review note, is
where it belongs). `pip-audit` clean on `mcp==2.0.0` + transitive deps at
this G6 (no known CVEs today) — this is a **supply-chain trust dependency
to re-check on every future dependency-audit cycle**, not a one-time
finding, the same way `CI → ECR → ECS`'s row already treats the container
supply chain generally.

**Assumption #1 still open, still not `#11`'s to close:** `StubTokenVerifier`
mirrors `#10`'s `X-Harness-Actor` stub exactly (any non-empty bearer token
= authenticated, no real verification of who's asserting it) — same G7
deployment blocker named in `#10`'s delta, unchanged by `#11`. `ISSUER_URL`/
`RESOURCE_SERVER_URL` default to `localhost` and are overridable via env
var for real deployment — configuring them for real is bundled into the
same G7 real-SSO work, not a separate gap.

## New boundary — GHCR registry → dev pull (GH-32 / ADR-013, 2026-08-19)

`ADR-013` decided (and this row was named as its own required follow-on,
not optional) to publish version-tagged, content-baked images to GHCR.
Structurally the same shape ADR-008 already modeled for the shared
skill-artifact registry (`Shared registry → BU build pipeline` row,
above) — same mitigations reused deliberately, not reinvented:

| Boundary | S | T | R | I | D | E | Mitigations | REQ/ADR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GHCR registry → dev `docker pull` | only CI (via the workflow's own `GITHUB_TOKEN`, no long-lived keys — same `CI → ECR → ECS` pattern) can publish a tag | published tags are immutable, `:latest` is never published (ADR-013's own extension of ADR-002's "no latest" invariant to images) | GHCR's own push/pull audit log (GitHub-hosted, same account as this repo) | content baked into the image is the same Internal-max doctrine already served by `#10`/`#11` — no new classification, no new data | a bad tag can't be "fixed in place" (immutable) — a corrected tag is a new publish, same as any other release | the registry adds a pull surface, not a write path back into the running service — pulling an image doesn't grant any tool/route access this repo doesn't already gate | served content is still sha256-manifest-verified at request time regardless of which build mode produced the image (`app/doctrine.py::read_file_verified`, unchanged) — **a tampered image still can't serve tampered content past the existing fail-closed integrity check** | `ADR-013`, reusing `ADR-008`'s registry mitigations |

**Not a new AI-specific threat** (no MCP/LLM-context change — GH-32 only
changes how the same content gets into the container, not what's served
or how). **Repo is public** (`gh repo view --json visibility`) — GHCR
publish requires no new secret; the workflow's default `GITHUB_TOKEN`
with `packages: write` is sufficient, itself a smaller credential surface
than provisioning a long-lived PAT would have been.
