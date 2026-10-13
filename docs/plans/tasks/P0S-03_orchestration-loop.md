# P0S-03 — Synthetic orchestration loop

## Status
In Progress

## Execution Metadata
- Type: backend
- Executor: worker agent
- Depends on: none
- Allowed scope: `repositories/caf-orchestration-worker/**`
- Out of scope: all other repositories
- Required skills: none
- Maximum repair attempts: 2
- Documentation impact: `docs/architecture/overview.md`, `docs/experiments/**`
- Verification commands:
  - `repositories/caf-orchestration-worker` -> `uv run pytest`
- Blocking conditions: CrewAI mode requires verified no-cost configuration

## Purpose
Run a bounded, observable synthetic plan, implementation, review, correction and deterministic gate sequence through the runtime protocol.

## Acceptance Criteria
- AC-1: Baseline asyncio mode completes and persists a structured artifact.
- AC-2: A negative finding or failed gate triggers bounded correction and reevaluation.
- AC-3: CrewAI mode is implemented and tested only if it can run without unapproved model access; otherwise report evidence and keep it pending.
