# CrewAI Factory (CAF)

CAF is an independent experiment in orchestrating Codex CLI and Claude Code as external coding agents with CrewAI. Its question is whether CrewAI adds measurable value over an equivalent Python `asyncio` workflow.

**Status:** the first synthetic P0 slice is verified: a provider-neutral runtime contract, sample fixture, asyncio baseline, CrewAI Flow mode, and external-worktree integration test. Host Codex/Claude adapters and an authenticated control API are implemented. Both CLIs passed separate no-tools smoke calls using existing profiles; code-changing CLI tasks remain untested. The provisional Compose `core` slice now starts API and PostgreSQL with healthy containers, reachable loopback endpoints and tested live task intake. A worker daemon, complete SPEC core group, UI, worker recovery and benchmark verdict remain pending. [SPEC.md](SPEC.md) is the authoritative source for the full target and acceptance criteria.

## Navigate

- [Documentation index](docs/README.md)
- [MVP scope and roadmap](docs/requirements/scope.md)
- [Architecture and service boundaries](docs/architecture/overview.md)
- [Data and contracts](docs/architecture/contracts.md)
- [Deployment and operations](docs/operations/local-development.md)
- [Security and tests](docs/development/verification.md)
- [Decisions and open questions](docs/architecture/decisions/0001-repository-and-runtime.md)
- [Repository publication procedure](docs/development/repositories.md)

The `repositories/` entries are independently versioned Git submodules with published initial commits. A fresh recursive clone succeeds. See [repository instructions](docs/development/repositories.md) and run `bash scripts/bootstrap.sh` in an existing checkout.

Run `python -m unittest discover -s tests/integration -p test_synthetic_fixture.py -v` from an initialized checkout to verify the synthetic workflow. Review the [experiment evidence](docs/experiments/2026-10-13-synthetic-baseline.md) and [traceability table](docs/requirements/traceability.md). The [service wrapper](scripts/services.sh) covers the tested API/PostgreSQL slice. See [local operations](docs/operations/local-development.md) and the [P0 implementation plan](docs/plans/2026-10-13-p0-vertical-slice.md).
