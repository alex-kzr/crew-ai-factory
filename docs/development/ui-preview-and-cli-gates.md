# UI inspection and remaining host CLI gates

Source: [SPEC sections 5, 9-12 and 14-16](../../SPEC.md). Status: **offline
preview and optional host-only one-Run read implemented; live integration and
full production CLI recovery open**.

## P0 UI preview

The `caf-web-ui` submodule now builds a React/TypeScript/Vite page. Its task
form validates the current `CreateTask` fields and prepares a JSON body; it
does **not** submit. Its Run inspector imports a local `RunStatus` JSON file
or loads a clearly labeled fabricated test example. It shows status, IDs,
timestamps and only known artifact gate/review fields. A `failed` Run with
`artifact.reason=orphan_unverified` is explicitly labeled quarantined and not
automatically retried. Missing fields are shown as unavailable. React renders
imported strings as text; arbitrary artifact content is not dumped.

An optional Node host server now exposes status, typed results, and a bounded
lease journal for exactly one configured Run. It keeps an existing API bearer
server-side, checks Host, binds to loopback, does not forward browser
credentials, and strips the opaque artifact from the status response. The
results projection is **not** secret redaction of free text; only view Runs
appropriate for local display. Loopback access does not authenticate a human
user. The server does not submit or cancel Runs, and its three separate reads
can race during a transition. One isolated PostgreSQL/API and same-origin
HTTP read passed on 2026-10-14; a visual browser acceptance test and human
identity authentication remain open. See the [inspection contract](../architecture/run-inspection-contract.md)
and [evidence](../experiments/2026-10-14-p0-live-run-and-crash.md).

The API still lacks a task list, service status and full workflow event
stream. This preview does not demonstrate P4 acceptance.

## Minimal filtered-environment CLI check

The filtered-environment status check passed for both installed CLIs on
2026-10-14 without printing auth output. No new credential was created.
For a repeat, verify that the existing host CLI profiles remain valid. With a
clean checkout, use the exact native
Codex executable recorded in [environment facts](environment.md) and the
resolved Claude executable; first verify both versions. Launch each CLI's
read-only login status command as a direct argument array with
`caf_agent_runtime.child_environment()`, an explicit working directory, a
short timeout and captured output. The established commands are `codex login
status` and `claude auth status`. Record only pass/fail, executable version,
exit category and whether the filtered environment excluded CAF worker and
model tokens. Do not print or store authentication material. A status check
would confirm login visibility, **not** successful model execution.

A normal Run exercised Codex implementation and Claude review, while a
controlled real Codex child crash and durable quarantine passed another
isolated check; see the
[measured result](../experiments/2026-10-14-p0-live-run-and-crash.md). These
measurements do not establish all provider process-tree behavior or complete
SPEC P0 acceptance.
