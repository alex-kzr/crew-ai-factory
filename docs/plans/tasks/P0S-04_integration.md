# P0S-04 — Integrate first milestone

## Status
To Do

## Execution Metadata
- Type: tooling
- Executor: umbrella integrator
- Depends on: P0S-01, P0S-02, P0S-03
- Allowed scope: `docs/**`, `scripts/**`, `tests/**`, `README.md`, `.gitmodules`, `repositories/*`
- Out of scope: unrelated projects
- Required skills: none
- Maximum repair attempts: 2
- Documentation impact: `docs/experiments/**`, `docs/development/**`
- Verification commands:
  - `.` -> `bash scripts/bootstrap.sh`
- Blocking conditions: child contract incompatibility

## Purpose
Pin tested child commits, execute a shared synthetic scenario from a fresh checkout, reconcile contracts, and record the observed result and remaining gaps.

## Acceptance Criteria
- AC-1: Umbrella gitlinks pin reachable child commits and bootstrap succeeds from a fresh checkout.
- AC-2: Synthetic scenario runs on the sample fixture and records review, correction, tests and final artifact.
- AC-3: Documentation distinguishes observed behavior from planned CLI/Compose/CrewAI behavior.
