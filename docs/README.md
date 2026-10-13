# CAF documentation

`SPEC.md` at the umbrella root is the authoritative requirements source. These pages organize it for implementation; where a design is unresolved, it is labeled **Decision pending** or **Proposed**. Do not read planned behavior as shipped behavior.

| Area | Page |
|---|---|
| Product, MVP, phases | [Scope](requirements/scope.md) |
| Requirement coverage | [Traceability](requirements/traceability.md) |
| Components, flows, diagrams | [Architecture overview](architecture/overview.md) |
| Typed data and interactions | [Contracts](architecture/contracts.md) |
| Host worker trust and queue transport | [Worker transport](architecture/worker-transport.md) |
| Proposed bounded HTTP check | [One-Run synthetic HTTP procedure](experiments/2026-10-13-scoped-http-procedure.md) |
| Repository ownership | [Repositories](development/repositories.md) |
| P0 execution | [Plan](plans/2026-10-13-p0-vertical-slice.md), [board](kanban.md), [environment facts](development/environment.md) |
| Experiment evidence | [Synthetic baseline](experiments/2026-10-13-synthetic-baseline.md), [Flow, CLI and API follow-up](experiments/2026-10-13-flow-cli-and-api.md), [P0 recovery and queued sample](experiments/2026-10-13-p0-recovery-and-code.md), [worker transport and daemon](experiments/2026-10-13-worker-transport-and-daemon.md) |
| Compose grouping and local operations | [Local development](operations/local-development.md) |
| Security, evaluation and acceptance | [Verification](development/verification.md) |
| Decisions and questions | [ADR 0001](architecture/decisions/0001-repository-and-runtime.md) |

The [original specification](../SPEC.md) includes the complete target deliverables and acceptance criteria. Update this index and the traceability table when requirements change.
