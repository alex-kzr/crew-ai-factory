# Proposed one-Run synthetic HTTP check

Status: **executed once on 2026-10-13 with explicit approval; temporary
tokens removed and processes stopped**. The steps below remain the procedure
for a separately approved repeat.
Source: [SPEC sections 5, 9-12 and 16](../../SPEC.md) and the
[worker transport boundary](../architecture/worker-transport.md).

## Approval and secret handoff

Ask the operator to approve one temporary, **15-minute**, test-only worker
grant for a single known Run. The API and worker will be temporary Windows
processes on the same host. The API will listen on `127.0.0.1:18123` after
checking that the port is available. It will connect only to the existing
`caf_queue_test_code` PostgreSQL on `127.0.0.1:55433`. The shared `caf`
database and core API at `127.0.0.1:8123` will remain untouched. The worker
will use `p0_synthetic_http`, which contains no Codex/Claude runtime call.
The operator should confirm the port, test database and one-Run scope; no
secret value needs to be entered in chat.

There is no available native local handoff facility that injects one secret
into both a Windows host process and this local API while hiding it from the
operator and Docker metadata. After approval, one local supervisor PowerShell
session can create random temporary API and worker bearer values in memory,
pass them through environment variables only to its two child processes and
remove them when those processes exit. Never place either value in a command
argument, terminal output, repository file, `.env`, Compose environment or
log. Anyone able to inspect either process environment while it runs can
read its token. This limitation is part of the approval decision.

## Exact sequence after approval

1. Start only `caf-p0-test-postgres-1`; retain its existing test volume. Load
   its test database password locally without printing it. Run the API's
   schema migration against the verified `caf_queue_test_code` DSN. Check
   that `18123` is free and that the core `caf` queue is empty.
2. Start a temporary host API with `CAF_DATABASE_URL` pointing to that test
   database and a new temporary `CAF_API_TOKEN`, bound by `uvicorn` to
   `127.0.0.1:18123`. Leave the worker grant absent. Submit one task through
   `/v1/tasks`: repository `caf-sample-app`, workspace ID
   `caf-synthetic-v1`, base revision
   `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`, provider `codex`,
   prompt `CAF_SYNTHETIC_DELAY_3_SECONDS`, max corrections `0`, and a
   synthetic acceptance criterion. Record its returned Task and Run IDs.
   The provider field is contract data; this worker uses `SyntheticRuntime`
   regardless of that field.
3. Stop that API process. In the same local supervisor session, create a new
   temporary worker bearer and restart the API with every required grant
   field: `CAF_WORKER_TOKEN`, `CAF_WORKER_ID=worker-caf-synthetic-01`,
   `CAF_WORKER_DATABASE=caf_queue_test_code`, the recorded
   `CAF_WORKER_RUN_ID` and `CAF_WORKER_TASK_ID`,
   `CAF_WORKER_REPOSITORY=caf-sample-app`,
   `CAF_WORKER_WORKSPACE_ID=caf-synthetic-v1`, the base SHA above,
   `CAF_WORKER_PROVIDER=codex`, and a timezone-aware
   `CAF_WORKER_EXPIRES_AT` 15 minutes ahead. An incomplete grant must prevent
   startup; an expired grant must return 503.
4. Start one host process running
   `python -m caf_orchestration_worker.p0_synthetic_http` with only
   `CAF_WORKER_API_URL=http://127.0.0.1:18123`, the same temporary worker
   bearer, `CAF_WORKER_ID`, and `CAF_UMBRELLA_ROOT` pointing at the
   CAF umbrella checkout. The worker maps `caf-synthetic-v1` to the
   checked sample submodule. It claims once and exits. Do not start the
   persistent daemon or any real CLI worker.
5. Check the scoped Run's terminal artifact and claimed/completed journal
   entries. Verify that the unrelated Run, if included as a negative control,
   remains queued; a wrong owner receives 403, a foreign Run ID receives 404,
   and the shared `caf` queue remains empty. Stop both temporary processes,
   clear their parent environment values, stop only the test PostgreSQL
   container and retain the volume for review. The grant also expires on its
   own; stopping the API immediately revokes it.

## Measured result, 2026-10-13

The one-shot host API and synthetic HTTP worker ran against the isolated
`caf_queue_test_code` database. The test Run was
`333cbc75-c7fe-48cd-a95f-5e2c3b270f9b` (Task
`57cb55cd-7824-4f6f-ad06-365d0e4b9041`). It ended `succeeded` at
attempt 1 with `execution_kind=bounded-synthetic-worker` and journal events
`claimed,completed`. The existing unrelated Run
`1a6b53f5-941f-41c9-9dce-8112df78b720` remained `succeeded` and could
not be read or renewed through the scoped worker routes (404 in both cases).
A different owner received 403; the intake API token received 401 at a worker
route. The shared `caf` database had zero Runs.

After stopping the scoped API, it was briefly restarted **without** a worker
grant. The old worker token then received 503. Both temporary API instances
and the one-shot worker exited; host port `18123` had zero listeners. Only
the pre-existing core API and PostgreSQL remained running. The isolated test
PostgreSQL container was stopped and its volume retained. Neither temporary
bearer value was printed or written to a file. The worker entrypoint uses
`SyntheticRuntime` and contains no model CLI invocation.

This proves a real loopback HTTP exchange and exact SQL claim scope for one
synthetic Run. It does not validate provider login under the new filtered
environment, full real-CLI recovery or unattended `core` worker startup. A
separate decision and fresh review are required before real CLI auto-dispatch.
