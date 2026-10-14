# Plan envelope diagnostic gate

Date: 2026-10-14. Requirements: [SPEC sections 9–12 and 16](../../SPEC.md).
This is an offline follow-up to the [plan-only schema gate](2026-10-14-plan-only-schema-gate.md).

## Measured boundary

The next approved plan-only Run, `57c6b656-dd20-4cd3-a6f7-3c9c3ac56fae`,
exited the Claude CLI with code 0. The adapter recorded
`response_source=invalid_envelope`, and the plan stage then reported
`empty_output`. This combination proves a diagnostic mismatch: rejection at
the envelope boundary was labeled as missing plan text downstream. It does
not identify which envelope property failed. Raw stdout was intentionally not
retained, so the exact provider response and original rejection reason cannot
be recovered. The isolated audit databases `caf_queue_test_plan_50f672fb`
and `caf_queue_test_plan_cef5ec95` remain preserved; neither was used in this
offline change.

## Offline contract and correction

The pinned Claude Code 2.1.296 `--help` confirms `--json-schema`,
`--output-format json`, `--tools ""`, `--permission-prompts none`, and
`--restricted`. The actual plan argv selects these flags and supplies the
schema as an argument array, without a shell. [Claude Code's programmatic CLI
documentation](https://code.claude.com/docs/en/headless#get-structured-output)
describes `json` as one result envelope and places the schema result in a
top-level `structured_output`; `stream-json` is the event stream. The
documentation does not require `type` or `subtype` tags in JSON mode. The
parser therefore accepts absent tags, checks known success values when tags
are present, and never substitutes textual `result` or a nested field for
top-level `structured_output`.

The runtime now rejects malformed UTF-8/JSON, duplicate keys, multiple JSON
values or trailing data, non-object roots, provider error flags/status,
unexpected tags, missing or wrong-type structured output, size excess, and
secretlike content with fixed reason codes. Deep JSON and overlong integers
also receive fixed malformed-JSON diagnostics. It records only fixed enum
values, JSON type categories, and a capped byte count; no raw content,
unknown field name, provider message, or transcript is persisted. An
exit-zero rejection is an agent failure with `response_source=rejected_envelope`.
The worker carries the allowlisted envelope reason to its terminal diagnostic
and marks `parser_outcome=not_run`; the plan parser is not called.

Synthetic single-JSON, JSONL, provider-error, missing-field, duplicate-key,
pathological-JSON, and worker queue fixtures cover the path. These tests prove
the offline adapter and worker behavior, not the shape of the earlier live
response or a successful Claude structured-output call.

Independent review found that an escaped lone Unicode surrogate could raise
`UnicodeEncodeError` during the structured-value byte count, bypassing the
fixed diagnostic. An offline follow-up classifies it as `malformed_json` with
`invalid_json` framing before persistence. High and low lone surrogates,
one valid surrogate pair, and the worker's `not_run` path have regression
tests. This is a parser robustness fix, not a finding about the prior Run.

## Next minimal experiment

After publishing and pinning the runtime and worker changes, run at most one
new no-tools, plan-only Run against a new isolated `caf_queue_test_*` database
and one exact, temporary Run grant. Use the existing Claude subscription, no
API-key fallback, zero corrections, and the same pinned sample base. Capture
only CLI exit code, response source, fixed envelope diagnostic, parser outcome,
stage count, and audit status. If the envelope is rejected, stop there and use
the fixed reason to choose a narrow offline correction. If it is accepted,
assess the local plan parser result before considering any coding Run. Preserve
the audit database and stop temporary processes. No Run, model call, grant, or
container start occurred for this offline correction.

## Single approved live check after publication

The runtime `e1982f807d85905999f0b710c1810c90b26003b5`, worker
`d85a61e56242a42ea2cb14e50e361f1ab64b1d74`, and umbrella
`0368502ed6b0f384b4b356c7ddfd09664e57cbca` were published and verified
on their `main` remotes in that order. The worker's installed runtime
provenance matched the pinned runtime SHA. One approved no-tools plan-only
Run used sample base `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`, one
temporary exact-Run grant, the existing Claude subscription, and isolated
database `caf_queue_test_plan_1fec3b0f`. Run
`71c55191-f6ff-490e-a8b6-fcac78d386b3` finished `failed` after one
attempt. Its only stage was `plan`; iterations were zero and no coding,
review, correction, diff, commit, or gate artifact was produced.

The safe terminal diagnostic is `category=envelope`,
`response_source=rejected_envelope`, `envelope.reason=root_type`,
`envelope.framing=single_json`, `envelope.root_type=array`, and
`parser_outcome=not_run`. The capped stdout count was 10,792 bytes. The
diagnostic shows a root-shape mismatch and confirms that the plan parser did
not mislabel this rejection as `empty_output`. It does not establish the
array's contents or why Claude Code emitted it; no raw response was saved.
Audit events were `claimed` and `completed`.

The worker and temporary API stopped, the temporary grant was revoked by
stopping that API, and the dedicated test PostgreSQL container stopped. Its
named volume remains attached, preserving the isolated database and audit.
The sample checkout stayed clean at the pinned base; the persistent CAF API
was not touched. The safe machine-readable evidence is outside Git at
`C:\Users\admin\Documents\Codex\2026-10-13\task-3\caf_plan_envelope_live_evidence.json`.
No second live attempt was made. Further work should inspect the static CLI
contract and actual argument assembly offline before requesting another Run.

## Offline investigation of the array root

The installed Claude Code 2.1.296 `--help` confirms the flags used by the
runtime. The plan argv is an argument array with `--print --verbose
--output-format json`, `--json-schema` containing an object-root plan schema,
`--tools ""`, `--restricted`, `--permission-mode dontAsk`,
`--permission-prompts none`, and `--no-session-persistence`. The worker sends
the prompt on stdin. On Windows, the supervised launcher passes child stdout
directly to the runtime pipe; the runtime collects bytes and decodes one JSON
value. Neither the supervisor nor the worker wraps stdout in an array.

The [official programmatic CLI contract](https://code.claude.com/docs/en/headless#get-structured-output)
describes `json` as a response with metadata and top-level
`structured_output`. It describes newline-delimited event objects for
`stream-json`. The [CLI reference](https://code.claude.com/docs/en/cli-reference)
defines `--verbose` as full turn-by-turn output, but does not specify an
array container for its combination with `--output-format json`. No inspected
official source establishes that a root array is a valid result envelope for
the pinned combination. The prior array contents were not retained; they
cannot be reconstructed or classified as events, results or an error.

The offline parser still rejects every root array. It now records only six
bounded shape fields: array length, non-object count, `type=result` count,
top-level `structured_output` count, error-indicator count, and whether a
sole result is last. Counts saturate at 1,001. Item contents, provider field
names and values never enter the diagnostic. Synthetic arrays with no result,
one terminal result, multiple results, and an error all remain rejected, with
the plan parser marked `not_run`.

If another Run is separately authorized, these fields are the minimum safe
evidence needed to distinguish a likely event collection from a different
array shape. Even a sole last result would remain rejected until an official
contract or equivalent installed vendor code confirms that container format
and its success/error rules. No new model call, grant or publication was made
for this investigation.

Independent review of the offline change identified one further no-tools
gap: `--tools ""` does not disable MCP tools under the [official CLI
reference](https://code.claude.com/docs/en/cli-reference). The runtime now
adds `--disallowedTools "mcp__*"` to its Claude argv; the installed 2.1.296
help confirms the option. This is a forward-looking gate correction and does
not prove whether any MCP tool was available in the measured Run. No new
live call was made to check the combined flags.

The installed help also states that `--strict-mcp-config` uses only servers
supplied by `--mcp-config`; the argv now includes the strict flag and supplies
no MCP config. This closes the startup configuration path independently of
the MCP deny pattern. The combination is checked in offline argv tests, not
through another model call.

## One approved array-shape diagnostic Run

After publishing and verifying runtime
`526c16ee658de6b955e2c860dd2c641d9e7d67ac`, worker
`117b5dec5c1e8e3090e73906d7665d539dfc028b`, and umbrella
`3832f473462bb375842207ff0bae87505af94d2f`, one approved plan-only
Run used sample base `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`,
the existing Claude subscription, an exact one-Run grant and isolated
database `caf_queue_test_plan_5a51c51d`. The worker installation matched the
published runtime SHA. A preflight checked the no-tools argv, including
`--tools ""`, `--disallowedTools "mcp__*"`, `--strict-mcp-config` and the
absence of `--mcp-config`. This checks the assembled flags; it is not direct
observation of Claude's internal tool availability.

Run `57847cc9-93a5-4cd6-a38f-ee0fe5402976` finished `failed` after one
attempt. Its only Flow stage was `plan`, with zero iterations. The fixed
diagnostic recorded `category=envelope`, `reason=root_type`,
`root_type=array`, `framing=single_json`, `response_source=rejected_envelope`,
and `parser_outcome=not_run`. The bounded array fields were length 5,
non-object count 0, `type=result` count 1, sole result position `last`,
top-level `structured_output` count 1, and error-indicator count 0. The
captured stdout byte count was 11,159. These facts are consistent with a
collection containing a terminal result, but do not establish the semantics
or contents of the other entries. The array was rejected; no plan value,
writer, review, correction, diff, commit or gate artifact was produced.

The journal events were `claimed` and `completed`. The temporary API and
worker stopped, removing access to the process-scoped grant; the test
PostgreSQL container stopped while its named volume and database remain for
audit. The temporary API port had no listener after cleanup, and the sample
checkout remained clean at the pinned base. The persistent CAF API was not
touched. The safe JSON evidence is outside Git at
`C:\Users\admin\Documents\Codex\2026-10-13\task-3\caf_plan_array_diagnostic_live_evidence.json`.
There was no second inference call. Root-array acceptance still requires a
verified vendor contract and explicit review before another live attempt.

## Documented transport prepared offline

The safe shape diagnostic does not establish an array contract, even though
the observed array had one last `type=result` object. The installed CLI help
and the [official structured-output example](https://code.claude.com/docs/en/headless#get-structured-output)
support `--output-format json --json-schema` for a single response envelope
whose top-level `structured_output` contains the schema-constrained value.
The example does not add `--verbose`. The [official streaming example](https://code.claude.com/docs/en/headless#stream-responses)
uses `--output-format stream-json --verbose` and describes separate event
objects with a last `result` line. It does not establish an array wrapper for
the prior JSON invocation, or the structured-output contract for combining
`stream-json` with `--json-schema`.

The runtime now omits `--verbose` only for operations with a structured
schema. This selects the documented JSON invocation for `plan`; unstructured
operations retain their existing streaming argv. The JSON decoder still
rejects every root array, multiple JSON values, duplicate keys, invalid
success/error indicators, provider errors, oversized values, and sensitive
structured output. The plan schema and worker gate are unchanged. Synthetic tests check
the argv and array rejection. This is an offline transport correction, not a
claim that Claude Code 2.1.296 has produced a valid envelope with this exact
invocation. A later live Run needs separate authorization and a fresh scoped
grant; the finished Run above must not be retried.

The worker's `pyproject.toml` and `uv.lock` now pin the local runtime commit
`5ddab9e6112ef81f1999cbfc6d0c2e8327c8b6bb` using the unchanged GitHub
source. An offline `uv lock` against that source cannot fetch an unpublished
commit. A temporary worker copy instead resolved the sibling runtime as a
local path and ran the Flow test suite on Python 3.12; this check does not
validate the committed Git source or the lockfile's Git fetch. After runtime
publication, verify the worker in a fresh clone with `uv lock --check` and
`uv sync --locked --python 3.12 --extra flow --group dev`, then run its tests before any
new live invocation. Do not publish the worker or umbrella gitlink first.
