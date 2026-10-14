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

**Current coverage:** documentation, tested synthetic runtime/workflow and sample fixture, synthetic CrewAI Flow parity, host CLI adapters, and an API/PostgreSQL slice with live readiness, authenticated task intake, guarded queue control and API-restart persistence. An isolated database and loopback API proved a disposable-child crash, lease expiry, durable quarantine and no replay. A later isolated gate completed one real Codex implementation, both acceptance suites and Claude approval in a single Run, exercised SQL-backed results/events and the one-Run host UI HTTP path, and verified real Codex child cleanup followed by quarantine and no replay in a separate Run. A production worker, complete SPEC core, connected P4 UI with human identity, full CrewAI Flow/correction pipeline in one Run and actual A/B/C benchmark remain pending. See [synthetic evidence](../experiments/2026-10-13-synthetic-baseline.md), [real CLI and UI gate](../experiments/2026-10-14-p0-live-run-and-crash.md), [UI boundary](../development/ui-preview-and-cli-gates.md) and [verification](../development/verification.md).
