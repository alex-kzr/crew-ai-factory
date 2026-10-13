# P0S-02 — Sample fixture

## Status
Done

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
  - `repositories/caf-sample-app` -> `python -m unittest discover -s tests -p test_baseline.py` (with `PYTHONPATH=src`)
- Blocking conditions: none

## Purpose
Provide a small runnable target repository and a reproducible coding task with fixed base revision and deterministic gates.

## Acceptance Criteria
- AC-1: Fixture baseline and requested behavior are documented without ambiguity.
- AC-2: Tests reproduce the task outcome without external services or credentials.
- AC-3: Git revision and command for identical experiment starts are recorded.

## Result

Completed 2026-10-13 — outcome: **verified**.

Verification commands:
- `repositories/caf-sample-app -> python -m unittest discover -s tests -p test_baseline.py` with `PYTHONPATH=src` — exit 0, 5 passed.
- `repositories/caf-sample-app -> python -m unittest discover -s tests -p test_discount_code.py` with `PYTHONPATH=src` — exit 1 as expected before the coding change.

Evidence:
- Pinned child commit and `discount-code-base-v1` tag `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`.
- [Synthetic experiment report](../../experiments/2026-10-13-synthetic-baseline.md).
