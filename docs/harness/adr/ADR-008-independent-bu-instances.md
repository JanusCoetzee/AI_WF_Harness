# ADR-008 — Harness ships as independent per-business-unit instances; core and skills version independently

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-07-25 |
| Deciders | janus (Driver) |
| REQs served | #8 (multi-team deployment of the harness) |

## Context

ADR-002 (accepted, G2 ratified 2026-07-19) chose a **single shared ECS
service**: one doctrine API + MCP endpoint, org-wide, with RBAC enforced at
the retrieval boundary to gate which callers see which content. That decision
assumed one org-wide doctrine lineage — "should be identical for every team
at a given version" — with cross-team access control as the open question,
which the RBAC amendment answered.

The stated operating model is different from that assumption: **each business
unit runs its own independent instance** of the harness, owned and
operated by that BU's Principal Engineer. Two governance facts follow:

1. **Core harness is one thing, semver'd** (`harness-core-vX.Y.Z`) — gates,
   stages, templates, standards, the constitution/operating-protocol split
   from ADR-003. A BU's instance runs *some* core version.
2. **Skills, hooks, and workflows are independently versioned units** a
   Principal Engineer layers on top of core, at whatever combination they
   choose. Upgrade timing for both core and skills is the Principal
   Engineer's call "within reason"; older versions are deprecated over time
   rather than forced.

This reframes the problem ADR-002 solved. Cross-BU RBAC is no longer the hard
part — separate deployments are already isolated by construction, no
in-application authz needed to keep BU-Finance from seeing BU-Retail's
content. The hard part ADR-002 didn't address: **how do N independent
instances each get a composed, versioned bill-of-materials (one core version
+ N independently-versioned skills) without becoming N silently-diverging
copies** — the exact drift problem ADR-002 was created to prevent, now
recurring one layer up.

If we don't decide this now, it lands mid-build on #10 (doctrine API +
authz), whose manifest schema (`docs/harness/adr/ADR-002-central-doctrine-
service.md` "Contracts") currently assumes one flat `version` field with no
concept of independently-versioned add-on skills.

## Options considered

### Option A — Keep ADR-002 as ratified: single shared multi-tenant service

- Sketch: no change. One ECS service serves all BUs; RBAC at the retrieval
  boundary gates which content each caller's role can see; all BUs run the
  same doctrine version.
- Pros: one infrastructure footprint to operate; no drift possible by
  construction (there's only one instance); already designed and partly
  built (#9 shipped).
- Cons: directly contradicts the stated model — Principal Engineers can't
  independently choose their own skill versions or upgrade cadence on a
  shared service without affecting every other BU on it; a single service
  outage blocks every BU simultaneously; RBAC-at-retrieval was solving a
  problem (cross-BU isolation) that independent deployment makes moot,
  while leaving the actual requirement (per-BU autonomy) unsolved.
- Risks: forcing the stated organizational model onto shared infrastructure
  it wasn't designed for.

### Option B — Fully independent instances, no shared distribution point

- Sketch: each BU stands up its own ECS instance from scratch — its own
  container build, its own copy of core harness source, its own skills,
  with no shared registry or release mechanism connecting them.
- Pros: maximum autonomy; zero coordination overhead to set up.
- Cons: this is Option A from ADR-002 ("git-only distribution") one layer
  up — every BU vendors core independently, a core fix becomes N pull
  requests with no way to know which BUs are even running which version;
  reintroduces the exact drift ADR-002 exists to prevent, just recursively.
- Risks: within 12 months, "BU-Finance is on core v1.2, BU-Retail forked
  core v1.0 and diverged" becomes unanswerable without manual survey.

### Option C — Independent runtime instances, shared versioned artifact registry

- Sketch: core harness and each skill/hook/workflow are built and published
  as independently-tagged artifacts (container images / git tags) to a
  shared registry (ECR + git tags, extending ADR-002's existing
  `harness-vX.Y` tag scheme to `harness-core-vX.Y.Z` plus a separate tag
  namespace per skill, e.g. `skill-<name>-vX.Y.Z`). Each BU's ECS instance
  is built by *composing* a pinned core version with whichever skill
  versions that BU's Principal Engineer selects — a per-instance manifest
  (`{core_version, skills: [{name, version}, ...]}`) becomes that BU's
  bill-of-materials, checked into that BU's own harness config (extending
  `harness.config.yaml`'s existing `doctrine_version` pin to a composed
  form). ADR-002's doctrine API/MCP contracts, read-only invariant, and
  integrity-check mechanics (sha256-pinned to signed tags) are **inherited
  unchanged** — they just now run once per BU instance instead of once
  org-wide, and the manifest schema gains a `skills` array alongside the
  existing `files` array.
- Pros: solves the actual requirement (independent per-BU cadence and
  ownership) without reintroducing drift-by-vendoring — a core fix is
  published once, and each Principal Engineer pulls it on their own
  schedule, but *what* they're running is always a known, auditable
  manifest, not a silent fork; RBAC-at-retrieval mechanics from ADR-002
  aren't wasted — they remain available for a BU that wants internal role
  gating within its own instance, just no longer load-bearing for cross-BU
  isolation; reuses #9's container work and most of #10's in-progress API
  design, only extending the manifest shape.
- Cons: two release trains now exist (core's and each skill's), and BU
  instances become a composition of both — auditing "what does BU-Finance
  actually run" requires reading a manifest, not just a single version
  number; deprecation of old core/skill versions needs an actual policy
  (who decides "deprecated," what happens to instances that don't move) or
  "within reason" has no enforcement teeth.
- Risks: without a deprecation policy, "within reason" drifts into "never" —
  the same unaudited-divergence risk as Option B, just slower to arrive.

## Decision

**Option C.** It's the only option that satisfies the stated model
(independent BU ownership, independently-versioned skills, BU-paced
upgrades) without recreating the N-copy drift problem ADR-002 was written to
solve. It also preserves the most work already done: #9's container and
#10's in-progress doctrine API/MCP contracts carry forward almost entirely —
the change is scoped to the manifest schema (add a `skills` array) and the
deployment topology (N instances instead of 1), not a redesign of the
service itself.

**Deprecation and drift management are a human governance function, not a
harness mechanism.** The Driver's ruling: version/deprecation policy for core
and skills is owned by governance (Principal Engineers + whatever oversight
body sits above them), not encoded as enforcement logic in the harness
itself. The harness's job stops at making the composition **legible** — a
readable manifest per instance, provenance on every served artifact — so
governance has something authoritative to act on; it does not extend to the
harness *forcing* an upgrade or blocking a stale instance. This mirrors the
existing pattern in this harness: gates require a human approver and a
`DECISIONS.log` line; they don't attempt to make bad human decisions
impossible, only visible and attributable. This is the same design choice
applied one layer up, at the fleet level instead of the single-change level.

This **supersedes ADR-002's single-shared-service topology**
(`docs/harness/adr/ADR-002-central-doctrine-service.md`) while explicitly
carrying forward its invariants: enforcement stays local, evidence stays in
each BU's own repos (never centralized), the service is read-only with no
write path, and content integrity is hash-pinned to signed tags. ADR-002's
RBAC-at-retrieval mechanism is retained as an available tool for
within-instance role gating, no longer required for cross-instance
isolation.

## Consequences

**Easier:** Principal Engineers get real autonomy over skill/hook/workflow
choice and upgrade timing without coordinating with other BUs; a core fix
ships once and is pullable by any instance on its own schedule; blast radius
of one BU's misconfiguration or outage doesn't reach another BU.

**Harder / new commitments:** #10's manifest schema needs to grow a `skills`
array before that work is finalized, which is a design change to
in-progress work, not a green-field addition; auditing "what is BU-X
running" now means reading a composed manifest per instance rather than
checking one shared version number; the harness's responsibility is bounded
at making that manifest legible and provenance-stamped — actually acting on
a stale or diverged instance is a governance process this ADR deliberately
does not encode, which means the harness cannot, by itself, prevent a BU
from silently running an unpatched core version indefinitely.

**Tripwire to revisit this ADR:** if it turns out governance needs the
harness to *do* more than expose a legible manifest — e.g. a stale instance
should refuse to serve, or should visibly flag itself as out-of-policy — that
crosses from "legible for humans to act on" into "harness enforces
governance decisions," which is a different, larger design (and arguably
crosses the same line ADR-002 drew against giving the service a write/control
path). Revisit here rather than quietly growing enforcement logic into what's
meant to stay a read-only, human-governed reporting surface.
