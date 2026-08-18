# Review Record — #11 (G5)

**This is a self-review under ADR-011's bootstrap override, not an
independent review — and it is the third and final use permitted under
ADR-011's own terms.** [`ADR-011`](../../adr/ADR-011-g5-bootstrap-override.md)'s
trigger #4 is a hard, countable tripwire: "Three or more G5s have been
passed under this override without any external review ever occurring."
`GH-9` was use #1, `GH-10` was use #2, this is **use #3 — the trigger
fires the moment this is logged as passed.** Per ADR-011's own consequence
section, that ends the bootstrap exception on the spot: no further T2/T3
G5 in this repo may use self-review under ADR-011 after this one, until a
second reviewer is actually found (trigger #1) or this ADR is explicitly
superseded. Recorded here, not just in `DECISIONS.log`, so the next
session reading this file directly sees it too.

## Reviewer pack

| Field | Value |
| --- | --- |
| Change | #11 — MCP tools (M2), commit `357ae91` (build) + `6c3a46a` (CI fix) |
| Tier | T2 |
| Evidence | 73 tests green (14 new), `app/mcp_server.py` 90% coverage, ruff clean, `pip-audit` clean (`mcp==2.0.0` + transitive deps) |
| Demo | Live MCP JSON-RPC protocol run (`PLAN.md` M2 demo record) — not just `pytest` |
| Area of least confidence | The SDK's OAuth resource-server middleware is doing real enforcement work this repo doesn't own or test directly (fail-closed depends partly on `mcp==2.0.0`'s own correctness, not only `app/mcp_server.py`'s) |

## Adversarial self-review (input to G5 — approves nothing on its own)

Same standard as `GH-10`'s: hunted by actually running the thing under
hostile inputs, not just reading the diff. Being the last use of this
shortcut made it worth spending more effort here, not less.

| # | Severity | Finding | Failure scenario | Disposition |
| --- | --- | --- | --- | --- |
| 1 | — | Checked and clean, live: empty-string bearer token, whitespace-only token, and a malformed `Authorization` header with no `Bearer` scheme all returned `401` before any tool code ran (SDK-enforced, `StubTokenVerifier.verify_token()` correctly returns `None` for blank tokens). Confirms fail-closed authn holds at the transport layer for the inputs an attacker would actually try first, not just the happy path already in `PLAN.md`'s demo record | | Accept |
| 2 | — | Checked and clean, live: an unknown gate name (`harness_get_gate {"gate": "NOPE", ...}`) returned a proper `isError: true` tool result over the real protocol (`"Error executing tool harness_get_gate: no gate named 'NOPE'..."`), not a raw crash or a 500 — confirms the `ToolError` boundary this module exists to enforce actually reaches the client correctly-shaped, not just that Python raises the right exception type internally | | Accept |
| 3 | Info | `harness_get_standard`'s `std_id` parameter is accepted but **ignored** — every call returns the full `docs/STANDARDS.md` regardless of what `std_id` is passed (confirmed live with a garbage `std_id`: `200`/success, full document back). This isn't a fail-closed violation or a security issue — the parameter's uselessness is already disclosed in the tool's own docstring ("there is one STANDARDS.md, not one file per STD-###") — but it's worth being honest that a caller passing a typo'd or nonexistent `std_id` gets silent success rather than any signal, a smaller version of exactly the "no silent fallback" principle ADR-002 states for `version` | Accept as documented. Considered fixing (validate `std_id` against a real `STD-###` pattern before returning) and rejected it: `STANDARDS.md` genuinely is one document, not N — inventing validation against a shape that doesn't map to real per-item granularity would be theater, not a fix. If `STANDARDS.md` is ever split per-`STD-###`, this tool's granularity should be revisited together with that split, not before |
| 4 | Info | `_resolve_manifest_or_error()` rebuilds the full manifest (sha256 of every catalogued file + a `git rev-parse`) on **every** tool call, same as `#10`'s already-accepted no-caching finding — now doubly relevant since two processes (`app/server.py` and `app/mcp_server.py`) both pay this cost independently, per request, with no shared cache between them | Accept, same disposition as `#10`'s finding #2 — real, not urgent, worth revisiting before either process sees real production call volume |
| 5 | — | Checked and clean: `name`/`gate`/`std_id` tool arguments are never used for filesystem access directly — `_get_by_kind()` only ever compares them against `Path(f["path"]).stem.lower()` for entries already enumerated from the manifest's own closed allowlist, so there's no path-traversal surface here at all, same safe-by-construction shape `#10`'s G5 confirmed for its HTTP route | | Accept |

## Traceability spot-check (manual — `req-trace.sh` limitation, same as `#10`'s G5)

`scripts/req-trace.sh` still can't see bare `#11` (its regex requires a
letter prefix before the digits) — confirmed by running it: no `#11` row,
same structural blind spot `#10`'s G5 first named. Still not filed as its
own issue.

| Claim | Traces to |
| --- | --- |
| Exactly 4 ADR-002 tools, no stdio, no write tools | `app/mcp_server.py` (four `@mcp.tool()` registrations, `transport="streamable-http"` hardcoded in `__main__`), `tests/test_mcp_doctrine.py::test_11_3_*`, live `tools/list` in `PLAN.md`'s demo record ✓ |
| Provenance on every fetch response | `app/doctrine.py::read_file_verified` (unchanged from `#10`), `test_11_1_*`, live `tools/call` result in the demo record ✓ |
| Unknown version/item → tool error, never silent fallback | `app/mcp_server.py::_resolve_manifest_or_error`/`_get_by_kind`, `test_11_2_*`, live `harness_get_gate {"gate":"NOPE"}` in this review's own adversarial pass (finding #2 above) ✓ |
| Fail-closed authz (denied item → no content) | `app/doctrine.py::is_allowed` (unchanged, reused directly — no parallel authz path), `test_11_4_*`, live 401s on empty/whitespace/malformed bearer tokens (finding #1 above) ✓ |
| Tamper → tool error, not content | `app/doctrine.py::read_file_verified` raising `IntegrityError`, caught in `app/mcp_server.py::_get_by_kind`, `test_11_5_*` — not re-driven live (same depth split `#10`'s demo record used; the mechanism is identical code to `#10`'s already-live-verified path, not new) ✓ |

## Human review (T2: one reviewer required — see override notice at top)

The adversarial self-review above is AI-drafted input to this gate — it
approves nothing on its own (CLAUDE.md §7; ADR-011 waives G5's
*independent-reviewer* requirement, not who renders the verdict).

| Reviewer | Verdict | Date |
| --- | --- | --- |
| janus (Driver — self-review under ADR-011 override, NOT an independent reviewer — **use #3 of 3, tripwire fires on pass**) | **pending Driver verdict** | — |

Diff size: `app/mcp_server.py` (new), `tests/test_mcp_doctrine.py` (new),
`app/requirements.txt`, `README.md` — within the ~500-line ceiling.
