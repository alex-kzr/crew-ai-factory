# Offline workspace binding and host recovery check

Date: 2026-10-13. Scope: P0 host worker boundary, following the
[scoped HTTP experiment](2026-10-13-scoped-http-procedure.md).

## Implemented

The one-shot synthetic and code worker entrypoints now require
`CAF_UMBRELLA_ROOT` and map an exact `workspace_id` to
`repositories/caf-sample-app` under that checkout. Unknown IDs and redirected
sample checkouts are rejected. The code fixture uses a freshly created private
directory under the verified host temporary root for each invocation; the
binding and execution path reject junctions, symlinks and locations within
the CAF checkout. The HTTP code worker accepts only the grant's one Run.
`CAF_REVIEW_SOURCE_RUN` is explicitly blocked before it attempts to read a
different Run. The direct-database continuation experiment remains historical
evidence, not a capability of the scoped HTTP entrypoint.

## Measured offline

The worker test suite completed with **46 passed, 3 skipped**. The skips are
host-dependent process or symlink checks. A real loopback HTTP test used a
dummy bearer, a separate worker process and the actual host runtime adapter
with a disposable Python child (no coding provider CLI). Terminating only the
worker caused Windows Job Object closure to stop the child. After the test
manually expired an in-memory lease, the fake API quarantined the Run and did
not replay the claim. Workspace binding tests cover exact IDs and a simulated
redirected temporary root. No new service token or provider call was used.

The recovery test's queue state is in memory and its lease expiry is injected.
It does not prove PostgreSQL recovery after a crash, a real provider CLI's
process containment, or an always-on worker. Separate earlier experiments
tested PostgreSQL lease/quarantine behavior and a real CLI fixture without
this combined transport and crash path. Those are still separate observations.

## Next gate

With explicit authorization, run one controlled crash test against the
isolated `caf_queue_test_code` database using a new short-lived, one-Run
loopback grant and a disposable Python child. Kill only that worker; verify
the child exits, the real lease expires, the Run is durably quarantined and
not replayed after API restart, and the shared `caf` queue stays empty. This
gate needs no provider CLI or model call. Real CLI login with the filtered
child environment and provider process recovery require later, separate
approval and measurement.
