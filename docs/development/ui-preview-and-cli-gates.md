# UI inspection and remaining host CLI gates

Source: [SPEC sections 5, 9-12 and 14-16](../../SPEC.md). Status: **offline
preview and optional host-only one-Run read implemented; live integration and
real CLI recovery open**.

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
can race during a transition. UI and server mock tests do not prove a live
PostgreSQL API integration. See the [inspection contract](../architecture/run-inspection-contract.md).

The API still lacks a task list, service status and full workflow event
stream. This preview does not demonstrate P4 acceptance.

## Minimal filtered-environment CLI check (planned, not executed here)

No new credential needs to be created **if** the operator's already verified
host CLI profiles remain valid. With a clean checkout, use the exact native
Codex executable recorded in [environment facts](environment.md) and the
resolved Claude executable; first verify both versions. Launch each CLI's
read-only login status command as a direct argument array with
`caf_agent_runtime.child_environment()`, an explicit working directory, a
short timeout and captured output. The established commands are `codex login
status` and `claude auth status`. Record only pass/fail, executable version,
exit category and whether the filtered environment excluded CAF worker and
model tokens. Do not print or store authentication material. A status check
would confirm login visibility, **not** successful model execution.

A later, separately bounded no-tools CLI smoke would be needed to verify
provider execution under the filtered environment. A still later controlled
crash test would need to confirm real CLI process-tree cleanup and durable
quarantine; the completed [disposable-child test]
(../experiments/2026-10-13-postgres-http-crash-restart.md) does not cover
provider processes. Neither later step is authorized or performed by this
document.
