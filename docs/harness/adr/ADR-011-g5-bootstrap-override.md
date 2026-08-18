# ADR-011 — G5's independent-reviewer rule is overridden during single-operator bootstrap, T1 excluded

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-08-18 |
| Deciders | janus (Driver) |
| REQs served | #9 (unblocks its G5), #8 (unblocks building `#10` on top of it) |

## Context

`gates/GATES.md:86` states G5's approver rule plainly: *"Reviewer(s) — must not
be the Driver; AI approval counts for nothing."* `#9` (the harness browser
container) shipped and `G4`-passed on 2026-07-19 with no G5 review since —
this repo currently has one human operator (the Driver) developing the
harness itself; there is no second reviewer to satisfy the rule as written.
Blocking on an independent reviewer that doesn't exist would stall the
harness's own bootstrap indefinitely, over a control this repo can't
currently meet by construction, not by negligence.

## Options considered

### Option A — Permanent waiver: G5's independent-reviewer rule doesn't apply to this repo

- Sketch: strike the requirement for this repo going forward, no revisit condition.
- Pros: zero ongoing friction.
- Cons: this repo isn't just internal tooling — it's the reference
  implementation other teams copy to learn what real gate discipline looks
  like (`README.md`'s whole pitch). Permanently gutting the one gate whose
  entire purpose is "the builder isn't the sole judge of their own work"
  undermines the credibility of every other gate this harness enforces on
  everyone else.
- Risks: this repo eventually needs real independent review (e.g. before
  recommending other teams trust `#10`/`#11`'s authz code) and a permanent
  waiver removes any forcing function to ever get there.

### Option B — Bounded override: applies now, named revisit trigger, T1 explicitly excluded

- Sketch: G5's approver rule is overridden **for T2/T3 work only**, for as
  long as this repo has a single operator and no second reviewer available.
  Every gate passed under the override is logged as such — not silently
  recorded as if independent review occurred. Named revisit triggers (below)
  end the override the moment any of them fire.
- Pros: unblocks real work now, honest in the audit trail about what
  actually happened (self-review, not independent review), matches this
  session's own established pattern for exactly this shape of decision
  (ADR-008/GH-21: accept a gap now, name concrete conditions to revisit it,
  never leave "pending" open-ended).
- Cons: someone has to actually notice when a trigger fires — same
  discipline gap ADR-008's own risk #6/#7 already named (governance-only
  drift control, not harness-enforced).
- Risks: a Driver could unconsciously lean on this to avoid ever finding a
  second reviewer. Mitigated by keeping T1 hard-excluded (the tier where
  four-eyes review is most load-bearing) and by logging every use, not just
  the first one, so the pattern is visible if it becomes a habit rather than
  a bootstrap accommodation.

### Option C — Ad hoc, one-off waiver for #9 only, re-decide every time this recurs

- Sketch: no durable policy; the next gate that hits this same problem asks
  the Driver again from scratch.
- Pros: minimal ceremony today.
- Cons: this will recur immediately (`#10`, `#11` are T2, same repo, same
  single operator) — re-litigating an identical decision repeatedly is
  exactly the friction this session's `DECISIONS.log` precedent (ADR-008,
  GH-21, GH-24) exists to avoid. Undocumented, repeated ad hoc exceptions
  are how "policy" quietly becomes "whatever we did last time," unaudited.

## Decision

**Option B.** Unblocks real work today without either permanently gutting a
real control (Option A) or creating unaudited, repeated one-off exceptions
(Option C). AI pair recommended B; Driver ratified it explicitly in-session
("we need an override since the Harness is still being developed... consider
THIS the approval you need") — which is itself the G5 approval this ADR
documents, for `#9`, under the terms below.

**Scope:** T2/T3 work in this repo only. **T1 is never covered by this
override** — if this repo ever takes on T1-tier work, independent review is
found before G5, full stop, no exception.

**Revisit triggers (any one ends the override):**
1. A second reviewer becomes available to this repo (even occasionally) — from then on, T2/T3 G5s use them, this ADR is superseded, not just ignored.
2. Any T1-tier work item is proposed for this repo.
3. This harness is recommended for adoption by a team/institution where G5's independent-review guarantee is being relied upon as already-proven (i.e. before telling anyone else "this passed G5 for real").
4. Three or more G5s have been passed under this override without any external review ever occurring — a concrete, countable tripwire against "bootstrap" quietly becoming permanent by inertia.

## Consequences

Easier: `#9`'s G5 is closeable now, `#10` can build on a foundation that's
at least self-reviewed rather than entirely unreviewed. Harder: every G5
passed under this override must say so explicitly in its review record and
`DECISIONS.log` line — "self-reviewed, ADR-011 override" is not the same
claim as "independently reviewed," and nothing should ever conflate them,
including future sessions reading `STATE.md` at a glance. Tripwire: trigger
#4 above (three uses) is a hard count — track it, don't let it pass silently.

## Trigger fired — 2026-08-18

**Trigger #4 has fired.** Three G5s have now been passed under this
override with no external review ever occurring: `#9` (use #1), `#10`
(use #2), `#11` (use #3 — Driver verdict "Approve",
[issue #11 comment](https://github.com/JanusCoetzee/AI_WF_Harness/issues/11#issuecomment-5323534667),
via [ADR-012](ADR-012-github-issue-approval-channel.md)). Per this ADR's own
terms, **the bootstrap override ends here.** No further T2/T3 work item in
this repo may self-review its G5 under this ADR. The next T2/T3 gate that
needs G5 either finds a real second reviewer (trigger #1, which supersedes
this ADR rather than extending it) or stalls at G5 honestly, rather than
spending a fourth use this ADR never authorized.
