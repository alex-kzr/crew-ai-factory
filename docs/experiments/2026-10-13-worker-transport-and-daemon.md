# Scoped worker transport and synthetic daemon check

Date: 2026-10-13. Source: [SPEC sections 5, 9-12 and 16](../../SPEC.md).

## Scope and observations

The API and worker now implement a loopback-only HTTP queue transport with a
separate worker token. The token is optional and the routes return 503 while
it is absent. Unit tests use dummy tokens. One opt-in in-process API test
against isolated `caf_queue_test_code` PostgreSQL verified claim, renewal,
completion and journal readback. This is not a live socket test against the
Compose API. See the [trust boundary](../architecture/worker-transport.md).

The Compose `p0-test-daemon` profile started a persistent synthetic worker
with a separate test PostgreSQL service. Both reached healthy. Test Run
`1a6b53f5-941f-41c9-9dce-8112df78b720` completed after a three-second
synthetic delay, at attempt 1, with claimed/completed journal entries. The
observed start-to-update interval was about 3.01 seconds.

During delayed Run `37581fae-0a94-47fd-9876-0d9c414656c5`, a controlled
kill of only the test daemon left the Run at attempt 1 with its claim and
lease intact. Starting the daemon again did not replay it. After forcing the
lease expiry for only that test Run, the daemon quarantined it as
`failed/orphan_unverified`, still at attempt 1, with claimed/quarantined
journal entries. A subsequent Run
`a5286fbd-2aca-412f-a796-d1a753432dad` completed at attempt 1 after the
same delay, showing the polling loop remained operational. The shared `caf`
database contained zero Runs during this test.

The daemon uses direct PostgreSQL and synthetic work in a dedicated test
database. It does not execute CLIs or prove that the host HTTP worker can
recover from every transport or process failure. A Docker kill did not
automatically restart the container in this observation; it was manually
started before lease expiry. No worker token was created or installed in the
live core. No automatic real CLI dispatch was enabled.

## Next gate

After an explicit temporary grant, run the [one-Run synthetic HTTP check]
(2026-10-13-scoped-http-procedure.md) using an isolated host API and test
database. Verify live loopback exchange, expiry and revocation. Provider login
under the new filtered child environment and host workspace mapping need
separate tests before any real CLI worker grant. The earlier daemon proof above
used direct PostgreSQL, so its observations are unchanged by the later API
grant implementation.
