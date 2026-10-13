# Product scope and implementation order

Source: [SPEC §§1–3, 7–8, 10, 14–16](../../SPEC.md). CAF evaluates CrewAI's orchestration of independent Codex CLI and Claude Code processes. The primary outcome is a controlled verdict against an equivalent Python `asyncio` baseline, not a generic agent platform.

## Target behavior

A user supplies a target repository and revision, constraints, and acceptance criteria. A planner creates a dependency DAG; developers work in isolated Git branches/worktrees; an integration stage combines changes; a reviewer examines the integrated diff; QA and deterministic gates test the integrated tree. Rework is bounded, failures become blocked, and all decisions and artifacts remain auditable. No automatic push, PR, or protected-branch merge without a configured approval policy. Role-to-provider assignments are configuration, not code constants.

## Initial MVP / P0

One complete vertical slice: bootstrap the independent repos; verified local CLI paths; a CrewAI Flow performing plan → implementation → review → bounded correction → tests on a sample app; commit, log and artifact capture; a tested `core` Compose group. The first synthetic contract slice now passes from a fresh checkout; it does not fulfill the real CLI, CrewAI Flow or Compose P0 proof of concept. See [experiment evidence](../experiments/2026-10-13-synthetic-baseline.md). It does **not** satisfy P0's runnable proof of concept.

## Subsequent phases

1. **P1 comparison:** Modes A (Crew-as-Tool), B (Flow-to-CLI), and C (`asyncio` baseline) use identical task schemas, adapters, workspace manager, fixtures, and scoring. Measure framework/API cost separately from subscription CLI use. Verify CrewAI manager configuration and capabilities experimentally.
2. **P2 parallel work:** DAG scheduling, parallel worktrees, integration branch, conflicts as tasks, gates and concurrency limits.
3. **P3 reliability:** persisted states/events, queue coordination, restart recovery, cancellation, orphan reconciliation and observability.
4. **P4 UI:** task intake, team editing, run graph/logs/artifacts, live events, service status and controls.

## Explicit initial non-goals

Kubernetes, multi-tenancy, billing, enterprise IAM, replacement coding CLIs, mandatory API keys for CLI execution, Temporal, RAG/vector stores, and a broker beyond Redis absent evidence. Git worktrees are not a security boundary.

## Next implementation slice

1. Record installed CrewAI, Codex, Claude, Git, Docker Compose and uv versions and authentication *availability* without exposing credentials.
2. Decide and test the runtime location and least-privilege credential/workspace access (see [ADR 0001](../architecture/decisions/0001-repository-and-runtime.md)).
3. Define common schemas and a tiny sample task; implement and test both CLI adapters with one verified non-interactive path each.
4. Add Postgres/Redis-backed persistence only as required by the first recovery path; implement the smallest runnable API, worker and Compose `core` slice.
5. Add Flow, review/correction/test loop and a reproducible E2E proof. Only then grow to comparison modes.
