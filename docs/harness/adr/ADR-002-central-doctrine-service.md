# ADR-002 — Harness doctrine is served centrally (ECS: browser + MCP); enforcement stays local; evidence stays in repos

| Field | Value |
| --- | --- |
| Status | Accepted (G2 ratified 2026-07-19, DECISIONS.log) |
| Date | 2026-07-19 |
| Deciders | janus (Driver) |
| REQs served | #8 (multi-team deployment of the harness) |

## Context

The harness must serve multiple teams and repos, not just this one. Three layers
with different physics are in play:

- **Doctrine** — gates, stages, templates, standards, operating model. Read-mostly,
  org-wide, should be identical for every team at a given version.
- **Enforcement** — hooks, verify loop, gate-check. Executes inside each
  developer's IDE session and each repo's CI; a remote service cannot block a
  local commit.
- **Evidence** — STATE.md, DECISIONS.log, dossiers, evidence bundles. The audit
  question is "what evidence existed *at this commit*" — only git answers that.

Target platform (stated by Driver): AWS ECS container; teams access from their
IDEs. If we don't decide, each adopting team copies the whole harness and the
copies drift — upgrades become N pull requests and no org-level view exists.

## Options considered

### Option A — Git-only distribution (vendor everything, no service)

- Sketch: this repo becomes a template repo with tagged releases; adopting repos
  copy doctrine + enforcement wholesale; upgrades arrive via each team's
  maintenance lane.
- Pros: zero infrastructure; works fully offline; doctrine and evidence versioned
  together in each repo.
- Cons: N-repo drift is structural; a doctrine fix is N pull requests; no
  cross-repo audit view; every repo carries ~40 doctrine documents it reads
  rarely (token and review noise).
- Risks: teams silently diverge; "which version of the gates were you on?" becomes
  archaeology.

### Option B — Central service is authoritative for everything

- Sketch: harness API on ECS owns doctrine *and* state: gate checks run
  server-side, DECISIONS.log and evidence live in a service database; repos hold
  only code.
- Pros: single point of upgrade; real-time org dashboard; nothing to vendor.
- Cons: **breaks both invariants.** Evidence decoupled from the commits it
  vouches for (a database row cannot prove what existed at commit `abc123`);
  enforcement cannot reach into IDE sessions — hooks are local by construction,
  so server-side "enforcement" is advisory.
- Risks: service outage blocks (fail-closed) or un-governs (fail-open) every team
  simultaneously; a second source of truth that `scripts/audit-decisions.sh` was
  built to prevent.

### Option C — Split: doctrine central, enforcement local, evidence in repos

- Sketch: one ECS service (this repo's read-only browser + an MCP endpoint)
  serves doctrine at pinned versions (`harness-vX.Y` git tags). Adopting repos
  vendor only the thin enforcement layer (`.claude/` hooks, `scripts/`,
  `harness.config.yaml` with a `doctrine_version` pin) and keep all evidence.
  CI gate enforcement ships as a reusable GitHub Actions workflow referenced by
  tag. A later harvester builds cross-repo views as a **derived, rebuildable
  projection** — never a source of truth.
- Pros: one upgrade point for doctrine; IDE sessions fetch templates/gates/
  standards on demand (token-cheap, always current for the pinned version);
  enforcement works offline (service down → sessions degrade to the vendored
  minimum, gates still enforceable); audit posture intact.
- Cons: two versioned things (doctrine tag + vendored enforcement layer); the
  thin layer still needs occasional vendored upgrades; real infrastructure to
  run (ECS, internal ALB, SSO).
- Risks: MCP-served content enters LLM context org-wide — a compromised service
  is a prompt-injection amplifier (mitigated in the threat model: content
  hash-pinned to signed git tags, fail-closed integrity check).

## Decision

**Option C.** The discriminating reason: it is the only option that satisfies
both non-negotiable invariants at once — *enforcement must execute locally and
offline* (IDE hooks, repo CI) and *evidence must be versioned with the code it
governs*. Option A satisfies the invariants but fails the stated goal
(multi-team scale without drift); Option B fails both invariants.

The AI (pair) recommended Option C; the Driver ratified it at G2 (2026-07-19,
DECISIONS.log), noting the harness will operate in a controlled environment.

### Amendment at ratification — RBAC (Driver requirement)

Access to certain doctrine/derived content will be role-restricted. The
architectural rule, fixed here because it cannot be retrofitted later:

> **RBAC is enforced at the retrieval boundary, never inside the model.** An
> LLM cannot be trusted to withhold content that has already entered its
> context; the only sound control point is what the service allows into
> context in the first place. The MCP/HTTP service — deterministic code behind
> SSO — evaluates the caller's identity and role claims *before* serving
> content. A model told "don't reveal X" is a policy suggestion; a service
> that never returns X is a control.

Mechanics: caller identity comes from SSO/OIDC claims (team, role) presented at
the ALB; every content item carries a classification/audience label in the
manifest; the service filters fail-closed (unlabeled = most restrictive).
Build slice 1 implements the authorization interface with an
all-authenticated-may-read-all policy (current doctrine is Internal-org);
tightening to real roles is then a policy change, not an architecture change.

## Contracts (defined before implementation)

All service interfaces are **read-only**; versions are always explicit — there
is no "latest" default, because an unpinned doctrine reference is an unauditable
one.

### HTTP doctrine API

- `GET /api/doctrine/{version}/manifest` → manifest JSON (schema below). 404 for
  unknown versions.
- `GET /api/doctrine/{version}/file?path={repo-relative path}` →
  `{ "path", "version", "sha256", "content" }`. The served `sha256` MUST match
  the manifest entry; on mismatch the service returns 500, never the content
  (fail-closed integrity — see threat model).
- `GET /api/health` → `{ "status", "doctrine_versions": [..] }` (extends the
  existing endpoint).

Manifest JSON Schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": ["version", "git_commit", "files"],
  "properties": {
    "version": { "type": "string", "pattern": "^harness-v[0-9]+\\.[0-9]+$" },
    "git_commit": { "type": "string", "pattern": "^[0-9a-f]{40}$" },
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["path", "sha256", "kind"],
        "properties": {
          "path": { "type": "string" },
          "sha256": { "type": "string", "pattern": "^[0-9a-f]{64}$" },
          "kind": { "enum": ["gate", "stage", "template", "standard", "doc"] },
          "title": { "type": "string" }
        }
      }
    }
  }
}
```

### MCP tools (same container, same content store)

| Tool | Input | Returns |
| --- | --- | --- |
| `harness_get_template` | `{ name, version }` | template content + `{version, path, sha256}` provenance |
| `harness_get_gate` | `{ gate, version }` | gate definition + evidence requirements |
| `harness_get_standard` | `{ std_id, version }` | standard text + threshold from config |
| `harness_search_doctrine` | `{ query, version }` | ranked `{path, title, excerpt}` list |

Every response carries provenance (`version`, `path`, `sha256`) so a session can
cite doctrine the way recon cites code. No write tools exist or will be added
without superseding this ADR.

## Consequences

- Easier: org-wide doctrine upgrades (move a tag), IDE access to current
  doctrine, cross-repo audit views (later, as a projection), thinner adopting
  repos.
- Harder: we now run infrastructure (ECS, ALB, SSO, ECR) and own a release train
  for doctrine tags; adopting repos gain a `doctrine_version` pin to maintain.
- Committed to: the service stays read-only (this extends ADR-001 from
  application level to platform level — read-only container filesystem,
  read-only repo mount); evidence never lives only in the service; MCP content
  is integrity-checked against signed git tags.
- Tripwire to revisit: (1) teams routinely need doctrine changes faster than the
  release train allows; (2) any pressure to add a write path to the service;
  (3) the integrity check gets disabled "temporarily"; (4) evidence starts being
  filed in the service instead of repos. Any of these supersedes or amends this
  ADR — not a quiet workaround.
