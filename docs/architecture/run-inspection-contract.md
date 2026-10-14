# P0 Run inspection contract

Source: [SPEC sections 5, 10-12, 14 and 16](../../SPEC.md). This is the
current implementation contract, not a claim of complete P0 or P4 operation.

All control API routes require the existing API bearer. `GET /v1/runs/{id}`
returns `RunStatus` with opaque `artifact` for trusted API clients. `GET
/v1/runs/{id}/results` returns a typed projection: `run_id`, `status`,
`artifact_present`, `execution_kind`, `reason`, `quarantined`, `gates`
(`suite`, `passed`, `exit_code`), `review` (`approved`, `findings`), and
`commit`. Unknown artifact keys, including raw diff and review transcript,
are omitted. The strings in known fields are **not secret-redacted**. `null`
means that structured evidence is unavailable; it does not mean a check
passed. `quarantined` is true only for failed Runs with
`reason=orphan_unverified`.

`GET /v1/runs/{id}/events?after_seq=0&limit=100` returns an array ordered by
ascending `seq`, with `seq`, `attempt`, `event`, `owner`, `terminal_status`,
and `created_at`. `after_seq` is exclusive; the limit is 1–100. The current
PostgreSQL `run_journal` records `claimed`, `completed` and `quarantined`.
This is lease history, not a full CrewAI Flow event stream. Unknown Run is
404. These endpoints have authenticated unit tests. Their SQL-backed HTTP
path passed one isolated Run check on 2026-10-14; see the [evidence](../experiments/2026-10-14-p0-live-run-and-crash.md).

The optional web host server accepts only GETs for one configured Run UUID
on loopback, uses an existing server-side API bearer, does not forward
browser credentials, and removes the opaque artifact from the status response.
It offers no human identity authentication or remote access. Reads of status,
results and events are separate snapshots; the UI rejects a status/result
mismatch and asks for a retry. Only use it for Runs whose known text fields
are suitable for local display. Task submission and cancellation remain
disabled in the UI.
