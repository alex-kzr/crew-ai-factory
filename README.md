# CrewAI Factory (CAF)

CAF is an independent experiment in orchestrating Codex CLI and Claude Code as external coding agents with CrewAI. Its question is whether CrewAI adds measurable value over an equivalent Python `asyncio` workflow.

**Status:** the synthetic P0 slice, host Codex/Claude adapters and authenticated control API have passed bounded checks. In a later isolated test, one queued Run produced a Codex edit, passed both sample suites and received Claude approval; another Run verified real Codex child exit, lease-expiry quarantine and no replay. The one-Run host UI read path passed an isolated HTTP check. These are fixture-specific gates. A production worker daemon, complete SPEC core group, full CrewAI Flow/correction in one Run, multi-user UI and benchmark verdict remain pending. [SPEC.md](SPEC.md) is the authoritative source for the full target and acceptance criteria.

The `caf-web-ui` submodule has a task JSON builder, local Run inspector and
optional host-only read of one configured existing Run through a server-held
API bearer. The example is fabricated. The page cannot submit or cancel Runs;
the host path passed one isolated API/HTTP read on 2026-10-14. See [its
boundary and checks](docs/development/ui-preview-and-cli-gates.md) and the
[measured evidence](docs/experiments/2026-10-14-p0-live-run-and-crash.md).

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
