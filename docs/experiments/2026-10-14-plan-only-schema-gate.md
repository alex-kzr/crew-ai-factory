# Plan-only schema contract gate

Date: 2026-10-14. Source: [SPEC sections 9-12 and 16](../../SPEC.md).
This note separates one measured Run from the subsequent offline contract fix.

## Measured plan-only Run

After worker `7656d4a35f66eadd3b9bac655be8befb59e1c3b9` and umbrella
`549b43107ac3bc1839058580ef3b0633123cfbe4` were published, one
approved plan-only Run used sample base
`e12f4d8293ea0dd8a5e18c3006af803c4d429b56`, an exact one-Run grant,
the existing Claude subscription, loopback API and isolated database
`caf_queue_test_plan_50f672fb`. Run
`cb4bd311-9d72-48d6-b680-7cd52d02be60` failed at its sole `plan` stage:
`plan_agent`, safe category `schema`, parser outcome `invalid_schema`, zero
iterations. No writer, review, correction, acceptance gate, diff or sample
commit occurred. Audit events were `claimed` and `completed`. Temporary
processes and the test PostgreSQL container stopped; the isolated audit
database was preserved. The safe JSON evidence is retained outside Git in the
Codex task directory.

The response text was not retained. `invalid_schema` does not identify a
field, type, value or the complete Claude response. No subsequent model call
was made for this analysis.

## Proven code mismatch and offline correction

The published planner told Claude to return a `steps` JSON object in its
prompt but did not supply a JSON Schema through the CLI. Its runtime extracted
the text `result` from a `stream-json` result event. The installed Claude Code
2.1.296 `--help` lists `--json-schema` and `--output-format json`, and the
[official programmatic CLI documentation](https://code.claude.com/docs/en/headless#get-structured-output)
describes `structured_output` as the schema-constrained value in a JSON
envelope. These are contract mismatches in the code, not a proven cause of the
measured failure.

The offline correction supplies an explicit schema for `plan`, selects JSON
envelope output, extracts `structured_output` only from a successful result
envelope, and still validates locally. Missing structured output and invalid
envelopes fail closed. The local validator requires exactly one `steps` array
with 1-8 nonblank strings of at most 300 characters each. It continues to
reject unknown fields, duplicate fields and wrong types. The schema is sent
only for plan operations; review remains on its existing path.

The persisted diagnostic adds only an allowlisted response source and one
schema error: a fixed keyword and code, path from `$`, `$.steps` or
`$.steps[]`, fixed expected/actual JSON type names, and a count of unknown
fields. It never records unknown field names or values, arbitrary provider
data, response text or CLI transcripts. Offline fake-process and Flow tests
cover successful and failing envelopes, Unicode size limits, schema failures
and absence of downstream stages.

## Next gate

The exact `--json-schema`/`--output-format json` combination with this schema
and subscription login is not live verified. If separately approved after
publishing the pinned runtime, worker and umbrella commits in that order, the
smallest test is one no-tools plan-only Run with a single exact grant, zero
corrections and a preserved isolated audit database. Inspect only the safe
response source, parser outcome and schema error code before considering a
coding Run. No additional Run, grant or model call was made in the offline
correction.

The later [envelope diagnostic gate](2026-10-14-envelope-diagnostic-gate.md)
records a separate exit-zero plan-only Run whose envelope was rejected and an
offline correction to the resulting misleading `empty_output` label.
