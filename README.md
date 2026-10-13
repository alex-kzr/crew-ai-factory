# CrewAI Factory (CAF)

CAF is an independent experiment in orchestrating Codex CLI and Claude Code as external coding agents with CrewAI. Its question is whether CrewAI adds measurable value over an equivalent Python `asyncio` workflow.

**Status:** documentation and local repository scaffold only. No application, Compose stack, adapters, tests, or benchmark results are implemented or verified yet. [SPEC.md](SPEC.md) is the authoritative source for the full target and acceptance criteria.

## Navigate

- [Documentation index](docs/README.md)
- [MVP scope and roadmap](docs/requirements/scope.md)
- [Architecture and service boundaries](docs/architecture/overview.md)
- [Data and contracts](docs/architecture/contracts.md)
- [Deployment and operations](docs/operations/local-development.md)
- [Security and tests](docs/development/verification.md)
- [Decisions and open questions](docs/architecture/decisions/0001-repository-and-runtime.md)
- [Repository publication procedure](docs/development/repositories.md)

The `repositories/` entries are independently versioned Git submodules with configured GitHub URLs. Their pinned initial commits have not been pushed, so a fresh checkout cannot initialize them yet. See [repository instructions](docs/development/repositories.md).

For now, documentation can be checked by following the relative links and comparing the [traceability table](docs/requirements/traceability.md) to [SPEC.md](SPEC.md). Runtime startup is not available.
