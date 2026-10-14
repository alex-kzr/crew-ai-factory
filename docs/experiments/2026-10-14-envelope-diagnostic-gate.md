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
