# SPEC traceability

This table maps each SPEC section to the development page that interprets it. [SPEC.md](../../SPEC.md) retains full normative detail; this table is an index, not a replacement copy.

| SPEC | Topic | Development page |
|---|---|---|
| §§1–3 | Mission, goals, non-goals | [Scope](scope.md) |
| §4 | Umbrella and child repositories | [Repositories](../development/repositories.md) |
| §§5–6 | Services and Compose groups | [Overview](../architecture/overview.md), [operations](../operations/local-development.md) |
| §§7–8 | Comparison modes and roles | [Scope](scope.md), [contracts](../architecture/contracts.md) |
| §§9–10 | Runtime adapter and Git workflow | [Contracts](../architecture/contracts.md), [overview](../architecture/overview.md) |
| §11 | Persistent data and telemetry | [Contracts](../architecture/contracts.md) |
| §12 | Security and operations | [Verification](../development/verification.md), [operations](../operations/local-development.md) |
| §13 | Technology choices | [Overview](../architecture/overview.md), [ADR 0001](../architecture/decisions/0001-repository-and-runtime.md) |
| §§14–16 | Phases, deliverables, acceptance | [Scope](scope.md), [verification](../development/verification.md) |
| §17 | Implementer instructions | [Scope](scope.md), [ADR 0001](../architecture/decisions/0001-repository-and-runtime.md) |

**Current coverage:** documentation, a tested synthetic runtime/workflow and sample fixture, a synthetic CrewAI Flow parity check, host CLI adapters with bounded Codex sample edits and a Claude review of an actual diff, and an API/PostgreSQL slice with live readiness, authenticated task intake, guarded queue control and API-restart persistence. An isolated test database proved worker-to-synthetic-runtime handoff and conditional artifact persistence. A production worker, complete SPEC core, UI, verified CLI crash recovery, persisted code-change artifact and actual A/B/C benchmark remain pending. See [synthetic evidence](../experiments/2026-10-13-synthetic-baseline.md), [follow-up evidence](../experiments/2026-10-13-flow-cli-and-api.md) and [verification](../development/verification.md).
