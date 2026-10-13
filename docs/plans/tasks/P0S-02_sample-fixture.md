# P0S-02 — Sample fixture

## Status
In Progress

## Execution Metadata
- Type: backend
- Executor: fixture agent
- Depends on: none
- Allowed scope: `repositories/caf-sample-app/**`
- Out of scope: all other repositories
- Required skills: none
- Maximum repair attempts: 2
- Documentation impact: `docs/experiments/**`
- Verification commands:
  - `repositories/caf-sample-app` -> `uv run pytest`
- Blocking conditions: none

## Purpose
Provide a small runnable target repository and a reproducible coding task with fixed base revision and deterministic gates.

## Acceptance Criteria
- AC-1: Fixture baseline and requested behavior are documented without ambiguity.
- AC-2: Tests reproduce the task outcome without external services or credentials.
- AC-3: Git revision and command for identical experiment starts are recorded.
