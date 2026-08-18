# ADR-012 — Driver verdicts on gates/decisions are requested via GitHub issue, rendered as an issue comment

| Field | Value |
| --- | --- |
| Status | Accepted |
| Date | 2026-08-18 |
| Deciders | janus (Driver) |
| REQs served | #8 (unblocks #11's G5 verdict without further chat-context overload), harness process itself |

## Context

Across one continuous work thread, pending Driver-verdict items accumulated
silently: five GC dossiers (GH-17–21), then #10's and #11's full build → G4
→ G5(→G6) cycles, landing on #11's G5 sitting at ADR-011's own trigger #4
tripwire (three self-reviewed G5s). Every step was logged faithfully to
`DECISIONS.log`/`STATE.md` — the audit trail is real and reconstructable —
but faithful logging is not the same as *surfacing*. Each individual ask
looked reasonable in isolation; the Driver's own words once it caught up:
"there is too much for me to track at this point... review overload."

The proximate cause: every approval-needing decision lived only inside one
chat session's scrollback, competing with everything else happening in that
session, with no durable, queueable, per-decision place for the Driver to
render a verdict at their own pace. The Driver then explicitly directed the
fix: file GitHub issues with clear explanations; they reply as a comment,
approve or decline.

## Options considered

### Option A — Status quo: verdicts rendered in-session, logged to DECISIONS.log

- Sketch: no change. The AI narrates what needs approval in chat; the
  Driver replies in the same conversation; the AI logs the verdict.
- Pros: fastest path when the Driver is actively driving a live session;
  zero extra artifacts.
- Cons: this is the exact mechanism that just produced the overload — every
  pending item lives only in one thread's memory, with no way for the
  Driver to process approvals asynchronously, at their own pace, or to see
  an aggregate queue of "what's actually waiting on me" without re-reading
  a long conversation.
- Risks: recurs identically the next time a session runs multiple
  build→gate cycles back to back — nothing about this option prevents the
  same pileup.

### Option B — One GitHub issue per Driver-verdict-needing decision; reply as an issue comment (Approve/Decline)

- Sketch: for any decision that needs the Driver's explicit verdict and
  isn't being rendered live in an active back-and-forth — a gate passage,
  an ADR ratification, a tripwire/override decision — the AI opens (or
  reuses, if the ticket already exists) a GitHub issue that states the ask
  plainly in the title, gives the evidence/options/recommendation needed to
  decide without re-deriving context, and asks for exactly one of
  Approve/Decline as a comment. The AI does not log a gate as passed (or a
  decision as accepted) until it has actually read that comment — not
  inferred from an adjacent chat message, not assumed from silence.
- Pros: async and queueable — the Driver works through a real GitHub
  notifications/issues list instead of chat scrollback; each decision gets
  its own durable, timestamped, attributable thread (comments are already
  exactly the audit record `DECISIONS.log` wants, just human-authored
  instead of AI-transcribed); scales past what a single session can hold in
  its head; forces the AI to write the ask *clearly enough to stand alone*,
  which is a real quality bar most in-session asks don't get held to.
- Cons: adds latency — a verdict isn't available the moment the AI wants to
  proceed to the next step, so build sequencing has to tolerate a gate
  sitting open; one more artifact per decision (an issue, sometimes a new
  one) instead of a chat message; needs a convention for what warrants an
  issue vs. a same-session nod, or every trivial clarifying question turns
  into a GitHub issue.
- Risks: the AI could file issues so numerous or so poorly explained that
  it recreates the overload one layer up (an issue queue nobody can get
  through instead of a chat thread nobody can get through) — the "clear
  explanation" requirement is load-bearing, not decorative.

### Option C — One batch issue per pending-approval group

- Sketch: instead of one issue per decision, the AI opens a single issue
  listing several pending items (e.g. "please review: #17 GC, #18 GC, #11
  G5") and the Driver comments once against the batch.
- Pros: fewer issues to open and close; one place to see everything at once.
- Cons: reintroduces exactly the problem being fixed — a single "approve"
  comment against a bundle can't cleanly express "yes to three of these, no
  to the fourth," and a Driver skimming a batch is the same rubber-stamp
  risk GATES.md's G5 "Fails if" clause already warns against for oversized
  diffs, applied to decisions instead of code.
- Risks: batches grow the same way chat threads did — the fix degrades back
  into the disease within a few sessions.

## Decision

**Option B.** It directly answers the Driver's own diagnosis and explicit
instruction, gives each decision a durable async home matching how
`DECISIONS.log` already treats one line as one attributable event, and
keeps per-decision granularity that Option C would have sacrificed back to
the same overload shape.

**Scope — an issue is warranted for:**
- any gate passage requiring a human approver that isn't being rendered
  live, in real time, in an active session with the Driver actually present
  and choosing to move fast (G4/G5/G6/G7, GC, and any ADR-011-style
  override/tripwire decision);
- any ADR ratification;
- any decision the AI is uncertain warrants a live ask vs. can wait —
  default to filing the issue, since the cost of an unnecessary issue is
  far lower than the cost of another chat-buried approval.

**Not required for:** routine in-session clarifying questions while the
Driver is actively driving a build step together with the AI in real time —
this ADR adds an asynchronous channel, it does not forbid the synchronous
one when the Driver is actually there and wants it.

**Mechanics:**
1. AI opens (or reuses) a GitHub issue. Title states the ask as a question
   a reader could answer without further context (e.g. "Approve #11's G5?
   Note: this is ADR-011 trigger #4"). Body: what's being asked, the
   evidence/links needed to decide, and the AI's own recommendation if it
   has one — stated as a recommendation, never as the decision itself
   (CLAUDE.md §7).
2. Driver replies as an issue comment: `Approve` or `Decline` (a reason on
   decline is expected but not schema-enforced here — human prose, not a
   form).
3. AI reads the actual comment (`gh issue view <n> --comments` or
   equivalent) before logging anything. A verdict is never inferred from
   an unrelated chat message, a session summary, or silence.
4. AI appends the `DECISIONS.log` line citing the issue and comment as the
   evidence trail, same as any other gate passage.
5. Closing the issue follows the same existing norm as everything else in
   this repo — not done without the Driver's separate go-ahead, since
   "Approve" on the *decision* is not the same instruction as "close this
   ticket."

## Consequences

**Easier:** the Driver processes approvals on their own schedule, in a
venue built for exactly this (threaded, notifiable, queryable, already
where every other ticket in this repo lives) instead of re-reading chat
scrollback to reconstruct what's still open; every future session can `gh
issue list --label pending-verdict` (or similar) and see the real queue
instead of trusting a session's own narrative that everything got
mentioned.

**Harder:** gate sequencing now has to tolerate real async latency — a
build can't assume the next gate's verdict arrives in the same sitting;
the AI carries a new discipline requirement (never log a verdict without
having actually read the comment) that's easy to accidentally shortcut
under time pressure, exactly the kind of shortcut this ADR exists to close
off; issue hygiene (labels, staying findable) becomes a small new
maintenance surface.

**Interacts with ADR-011:** does not supersede it and does not, by itself,
satisfy trigger #1 (a second reviewer becoming available) — an async
comment from the same single Driver is still self-review, just on a better
channel. #11's G5 verdict, whenever rendered, is still use #3 of 3 and
still fires ADR-011's trigger #4 the moment it's logged as passed,
regardless of which channel carried the "Approve."
