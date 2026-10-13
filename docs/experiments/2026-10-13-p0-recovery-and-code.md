# P0 recovery and queued sample follow-up

Date: 2026-10-13. Source: [SPEC sections 9–12 and 14–16](../../SPEC.md).
The observations below are bounded tests, not acceptance of the complete P0
deployment.

## Process and lease failure gates

- Windows runtime tests killed only their disposable Python runtime host. Its
  Job Object closed and its test-owned child stopped. Another fixture requested
  `CREATE_BREAKAWAY_FROM_JOB`; Windows created the child, but `IsProcessInJob`
  reported that it remained in this Job and cancellation stopped it. The
  complete runtime suite passed **44 tests**. This tests the ordinary child
  process path on this host; it is not a claim of universal security isolation.
- In a separate `caf_queue_test_*` PostgreSQL database, a test worker claimed
  one Run and exited with `os._exit(23)`. The `running` lease and `claimed`
  journal entry survived that process exit. A different worker could not claim
  the Run; after the test advanced its lease to expired, quarantine recorded
  `failed/orphan_unverified`, appended `quarantined`, and still did not replay
  the task. Four isolated live API tests passed. The journal writes claim,
  completion and quarantine in their respective state transactions.
- A `ProcessTreeCleanupError` now propagates through the workflow and the
  dispatcher, leaving the claim unacknowledged. The worktree is preserved if
  cleanup cannot be verified. No test killed a user process or restarted
  Windows.

## Isolated Compose worker

The `caf` Compose project gained an opt-in `p0-test` one-shot
`synthetic-worker` service. It uses the normal lease-aware dispatcher, checks
its actual connected database name before claiming, executes only the
synthetic runtime and writes a labeled artifact. Run
`01cc98bd-3120-40eb-8095-c1b417de9987` in
`caf_queue_test_p0_20261013_1` completed once with attempt 1 and
`claimed → completed` journal entries. A second container invocation returned
`empty`. The shared `caf` database still had zero Runs. This proves a
containerized PostgreSQL queue → worker → runtime path on a synthetic task;
the service is one-shot and does not run coding CLIs.

## Queued real sample code

The separate `p0-code-test` PostgreSQL service exposed only loopback port
55433 for an opt-in host worker. The worker guarded the test database, clean
sample checkout and exact base revision
`e12f4d8293ea0dd8a5e18c3006af803c4d429b56`, and used an external Git
worktree. No CLI credentials or worktree were mounted into Docker.

Three bounded queued Codex implementation attempts each produced a small diff
and passed both sample acceptance suites. Run
`954d5f8d-8d05-417b-8257-fec92ac018bc` failed because the worker's Git
porcelain parser stripped a leading status space; a regression test now covers
that case. Run `e39740f6-69b9-4fe7-affb-d9fd5f1ebda4` saved a passing diff
but failed strict review-output parsing. Run
`526c0a4c-b72c-4f8e-92b6-f5fad58bf2cc` saved the diff and a structured
Claude rejection: its no-tools review prompt referred to a requirements file
the reviewer could not read. These Runs remain terminal failed records; none
was replayed.

Run `83405339-0e91-4a78-af3d-2a135f9e0a25` reused **exactly** the saved
diff from the third Run, recorded `source_run_id`, applied it in a fresh
worktree, reran both passing suites, and gave Claude the full requirements in
the no-tools review prompt. The stored verdict is `approved=true` with no
findings. The Run is `succeeded`, attempt 1, with `claimed → completed` journal
entries and local commit `f9a12f770727351443fb25cfbaff6decfaf359bf` on
branch `caf-queue-experiment-834053390e91`. The worktree was removed; the
sample checkout and umbrella gitlink remain at the fixture base. The source
and continuation diffs compare equal. The continuation did not invoke Codex
again. Its full artifact, patch and review were exported to this task's local
output directory as `caf-queued-code-artifact.json`, `caf-queued-code.patch`
and `caf-queued-review.json`. The branch was not pushed or merged.
After exporting, only the separate test PostgreSQL container was stopped and
started again; the Run status, commit SHA and both journal entries remained
readable from its dedicated volume. This tests a normal database-container
restart, not an abrupt host failure.

The worker suite passed **35 tests**; two opt-in live database tests were
skipped in that local run. The Compose synthetic proof and real sample proof
used different, isolated test databases. The shared CAF queue had zero Runs
afterward.
The separate `p0-code-test` PostgreSQL container was stopped after export;
its `caf_p0_test_data` volume remains for inspection. The synthetic test
database `caf_queue_test_p0_20261013_1` remains namespaced inside CAF
PostgreSQL. Neither contains tasks in the shared `caf` database.

## Limits and remaining P0 gates

This host fixture uses the existing user CLI authentication and a Codex
`workspace-write` worktree. A Git worktree is not a filesystem or network
security boundary; this experiment does not authorize untrusted shared-queue
tasks or prove all possible descendant processes are contained. The `core`
profile still contains only API and PostgreSQL. There is no always-on
production worker, host runtime readiness endpoint, secure queue transport to
the host, or tested full-group restart. The current real-code path is one-shot
and fixture-specific. The real run did not use CrewAI Flow for plan/correction,
did not exercise a negative-review correction in one Run, and did not test
parallel integration. Mode A/B/C comparison, full persistent SPEC entities,
UI/observability groups and complete service-group commands remain open.

The next deployment decision is the host runtime/worker boundary: expose a
least-privilege authenticated queue transport to a host worker, or establish a
separately verified container credential and filesystem isolation policy.
Until then, automatic dispatch from the shared CAF database stays disabled.
