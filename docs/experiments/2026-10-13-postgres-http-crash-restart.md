# Scoped HTTP and PostgreSQL crash/restart check

Date: 2026-10-13. This is one explicitly approved P0 test in the isolated
`caf_queue_test_code` database. Source requirements: [SPEC sections 9-12 and
16](../../SPEC.md). It follows the [offline process check]
(2026-10-13-offline-workspace-and-recovery.md) and the [one-Run HTTP
check](2026-10-13-scoped-http-procedure.md).

## Test boundary

- Started only the existing `caf-p0-test-postgres-1` test container, retaining
  its volume. The shared `caf` API and database were not restarted or changed.
- Bound a temporary API to `127.0.0.1:18123` with a newly generated 15-minute
  grant for one Run, Task, owner, repository, workspace ID, base revision and
  provider. Tokens existed only in the supervisor and child process
  environments; their values were not printed or saved.
- Used the real `WorkerAPIStore`, `dispatch_once`, host `CodexRuntime` process
  containment and PostgreSQL store. The runtime command was replaced with a
  disposable Python sleep process. No Codex or Claude executable or model was
  called. The child confirmed that it did not inherit `CAF_WORKER_TOKEN`.
- Killed only the test worker after the claim and child startup, then stopped
  the temporary API. Waited for the **real database lease** to expire, without
  editing its timestamp. Restarted the same scoped API and requested scoped
  quarantine and a second claim.

## Measured result

Run `5c0776cd-f904-4de6-8cf1-a5884ee35344`, Task
`c42e394a-579f-4ac1-ba8e-4ea7f71b148a` reached `running`, attempt 1,
with an active lease. After the worker was killed, Windows Job Object closure
stopped the child. PostgreSQL then reported the lease expired while the Run
was still `running`. After API restart, scoped quarantine returned exactly
this Run. PostgreSQL readback showed `failed`, attempt 1,
`artifact={"reason":"orphan_unverified","attempt":1}`, no lease owner or
expiry, and journal events `claimed, quarantined`. A further quarantine
returned no Runs and another claim returned none: the Run was not replayed.

The API was restarted once more without the worker grant; the former worker
client received HTTP 503. The shared `caf` Run count was **0 before and
after**. The temporary API and test worker exited, the test PostgreSQL
container was stopped, the temporary child/scripts were removed, and port
`18123` was free. The test database volume retains the Run and journal for
inspection. No token value was retained in this evidence.

## Limit

This verifies the combined loopback transport, durable lease, API restart,
quarantine and no-replay path for one disposable process. It does not verify
real provider CLI authentication or its survival/cleanup behavior, a
persistent production worker, or complete SPEC restart/resume semantics.
