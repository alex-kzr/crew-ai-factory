# CAF implementation board

Plan: [P0 synthetic vertical slice](plans/2026-10-13-p0-vertical-slice.md).

## In Progress
- Resolve Codex CLI execution authentication on the existing profile and verify a real isolated code change.
- Connect queued API runs to an actual worker with durable claim/completion and tested restart behavior.

## To Do
- Start and health-test the provisional `caf` API/PostgreSQL Compose slice when container execution is permitted; then add the real worker/runtime boundary.
- Compare CrewAI Modes A/B with the baseline on identical fixtures once model configuration is verified.

## Done
- [P0S-01 Runtime contract](plans/tasks/P0S-01_runtime-contract.md)
- [P0S-02 Sample fixture](plans/tasks/P0S-02_sample-fixture.md)
- [P0S-03 Synthetic orchestration loop](plans/tasks/P0S-03_orchestration-loop.md)
- [P0S-04 Integrate first milestone](plans/tasks/P0S-04_integration.md)
- Publish and verify six initial repositories; fresh recursive clone succeeded on 2026-10-13.
- Implement and test host CLI adapters (31 tests; Claude no-tools smoke passed; Codex execution remains blocked).
- Implement CrewAI Flow Mode B over the shared synthetic workflow (17 tests, three parity scenarios).
- Implement authenticated API task intake and a provisional API/PostgreSQL Compose definition (tests/build/static configuration passed; live startup pending).
