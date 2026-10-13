# P0S-01 — Runtime contract

## Status
In Progress

## Execution Metadata
- Type: backend
- Executor: runtime agent
- Depends on: none
- Allowed scope: `repositories/caf-agent-runtime/**`
- Out of scope: all other repositories
- Required skills: none
- Maximum repair attempts: 2
- Documentation impact: `docs/architecture/contracts.md`
- Verification commands:
  - `repositories/caf-agent-runtime` -> `uv run pytest`
- Blocking conditions: none

## Purpose
Create an importable typed provider-neutral runtime package and synthetic adapter. Preserve a clear boundary for future real Codex/Claude adapters.

## Acceptance Criteria
- AC-1: Synthetic execution emits deterministic structured result and events with correlation IDs.
- AC-2: Status/cancellation and failure classifications have meaningful tests.
- AC-3: No real CLI, credentials or runtime worktree is required.
