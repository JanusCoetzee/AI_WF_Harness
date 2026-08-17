# ADR-010 — T3 collapses CHANGE.md's FinServ-only fields inline, not via a second template file

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-08-18 |
| Deciders | janus (Driver) |
| REQs served | GH-28 |

## Context

`templates/CHANGE.md`'s FinServ-inherited fields — **Linked records**,
**Timing constraints**, and the conditional **Regulated / reported outputs**
section — produced zero value on a real T3 change (AU_YEAR_9_MATH's CHG-001,
`docs/RETROS/RETRO-2026-08-18.md`): every one was answered "none" or deleted
outright, which is what any T3 change on a non-regulated repo will answer,
every time, forever. The template's own instruction ("'none' only after
checking") is correctly strict for T1 and pure overhead for T3. Question:
how does a T3 change get a lighter version of these fields without weakening
them for T1/T2, where they're load-bearing?

## Options considered

### Option A — Separate `templates/CHANGE-T3.md` file

- Sketch: a second, shorter template; `/harness-change` selects it when
  `harness.config.yaml`'s tier is T3.
- Pros: cleanest read for a T3 change — nothing conditional to skip past.
- Cons: **no precedent for a template-per-tier in this harness**, and it's a
  drift risk the harness has specifically avoided elsewhere — every future
  improvement to `CHANGE.md` (a new field, a reworded prompt) now has to land
  in two files or the T3 copy silently rots. GH-15/GH-25 this session were
  both about exactly this class of drift (a doc going stale because a
  sibling doc changed and nobody updated both).
- Risks: the two templates diverge in ways nobody notices until a T3 change
  is promoted to T1/T2 (`harness.config.yaml`'s own rule: "T3 output cannot
  be promoted without re-tiering") and the CHANGE.md underneath it turns out
  to have skipped fields the promotion should have caught.

### Option B — One template, tier-conditional inline instruction (matches `THREAT-MODEL.md`'s existing precedent)

- Sketch: `templates/CHANGE.md` stays a single file. Add an instruction next
  to the three FinServ-heavy fields: at T3, collapse them to one line
  (`Regulatory/audit surface: none (T3 — see harness.config.yaml)`) unless
  something in scope is actually reportable, in which case answer the full
  fields as normal. Exactly the pattern `templates/THREAT-MODEL.md` already
  uses (`| Tier | T1 (full STRIDE) / T2 (boundary table only) |` — one file,
  tier picks the depth).
- Pros: single source of truth, zero drift risk, consistent with the only
  existing precedent for tier-scaled template depth in this harness.
- Cons: `CHANGE.md` reads slightly more conditionally than a dedicated T3
  file would — a small readability cost, not a correctness one.
- Risks: none identified beyond the readability cost above.

### Option C — Skill-level shortcut, template untouched

- Sketch: leave `templates/CHANGE.md` as-is; teach `harness-change`'s
  `SKILL.md` to collapse the three fields itself when tier is T3.
- Pros: template stays maximally simple.
- Cons: anyone filling `CHANGE.md` by hand (not via the skill) never sees
  the shortcut — the template is supposed to be self-explanatory per
  CLAUDE.md §3 ("schemas as guardrails, not prose" extends to templates
  being usable standalone), and this option breaks that.
- Risks: the shortcut silently stops applying the moment someone drafts a
  CHANGE.md without going through the skill, which is common (this session
  drafted several dossiers directly).

## Decision

**Option B.** It's the only option with a real precedent in this harness
(`THREAT-MODEL.md`'s tier-conditional depth) and the only one that doesn't
create a second file to keep in sync — Option A repeats a drift mistake this
session already found and fixed twice (GH-15, GH-25). Option C fails the
template-must-be-self-explanatory standard.

## Consequences

Easier: T3 changes (the harness's own adoption case, AU_YEAR_9_MATH) stop
paying FinServ-audit ceremony that's never true for them. Harder: nothing
new — the collapse is opt-in-by-tier, T1/T2 behavior is byte-for-byte
unchanged. Tripwire: if a T3 change is ever promoted to T1/T2
(`harness.config.yaml`'s own re-tiering rule), the promotion step must
explicitly re-expand the collapsed line back to the full three fields — name
this in `/harness-change`'s Mode B (repair) guidance if promotion-from-T3
ever actually happens; not built speculatively now.
