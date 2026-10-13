# CAF implementation board

Plan: [P0 synthetic vertical slice](plans/2026-10-13-p0-vertical-slice.md).

## In Progress
- Preserve and verify a complete queued code-change artifact with a structured cross-provider review and commit from an isolated worktree.
- Resolve Windows orphan-child cleanup, then connect queued API runs to a bounded host worker and real runtime with tested restart behavior.

## To Do
- Add the production worker/runtime boundary to the API/PostgreSQL Compose slice; verify cancellation, lease heartbeat and recovery.
- Compare CrewAI Modes A/B with the baseline on identical fixtures once model configuration is verified.

## Done
- [P0S-01 Runtime contract](plans/tasks/P0S-01_runtime-contract.md)
- [P0S-02 Sample fixture](plans/tasks/P0S-02_sample-fixture.md)
- [P0S-03 Synthetic orchestration loop](plans/tasks/P0S-03_orchestration-loop.md)
- [P0S-04 Integrate first milestone](plans/tasks/P0S-04_integration.md)
- Publish and verify six initial repositories; fresh recursive clone succeeded on 2026-10-13.
- Implement and test host CLI adapters (34 tests; separate no-tools Claude and explicit-path Codex smokes passed).
- Implement CrewAI Flow Mode B over the shared synthetic workflow (17 tests, three parity scenarios).
- Implement authenticated API task intake and a provisional API/PostgreSQL Compose slice; live startup, readiness, bearer auth, idempotency and API-restart persistence passed.
- Implement transactional PostgreSQL queue claim, lease renewal and owner-guarded completion; isolated live database tests passed.
- Prove one queue-to-synthetic-runtime handoff in a dedicated test database; persist a labeled JSON artifact without starting a CLI or draining the shared CAF queue.
- Add guarded API cancellation and expired-lease quarantine; test claim/ACK/cancel/idempotency in isolated PostgreSQL and worker unit tests.
- Prove one bounded Codex sample code edit in an external worktree with both acceptance suites passing, and a separate Claude no-tools review of the actual diff returning `approved=true`. Neither experiment wrote to the CAF queue.
