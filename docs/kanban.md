# CAF implementation board

Plan: [P0 synthetic vertical slice](plans/2026-10-13-p0-vertical-slice.md).

## In Progress
- Verify real isolated Codex/Claude code changes and cross-provider review using the now-explicit CLI executable selection.
- Connect queued API runs to an actual worker with durable claim/completion and tested restart behavior.

## To Do
- Add the real worker/runtime boundary to the now-tested API/PostgreSQL Compose slice; verify claim, cancellation and recovery.
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
