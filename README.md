# CrewAI Factory (CAF)

CAF is an independent experiment in orchestrating Codex CLI and Claude Code as external coding agents with CrewAI. Its question is whether CrewAI adds measurable value over an equivalent Python `asyncio` workflow.

**Status:** the first synthetic P0 slice is verified: a provider-neutral runtime contract, sample fixture, asyncio baseline, CrewAI Flow mode, and external-worktree integration test. Host Codex/Claude adapters and an authenticated control API are implemented. A bounded Codex edit on the sample fixture passed both acceptance suites; Claude approved its saved diff with no findings, and the reviewed change is a local, unpushed sample commit. This isolated CLI experiment is not a queued production run. The provisional Compose `core` slice starts API and PostgreSQL with healthy containers, reachable loopback endpoints, tested task intake, cancellation and transactional queue operations. A test-only worker bridge and an executor-neutral lease-aware dispatch boundary passed isolated database tests. A production worker daemon, verified orphan CLI cleanup, complete SPEC core group, UI and benchmark verdict remain pending. [SPEC.md](SPEC.md) is the authoritative source for the full target and acceptance criteria.

The `caf-web-ui` submodule has a task JSON builder, local Run inspector and
optional host-only read of one configured existing Run through a server-held
API bearer. The example is fabricated. The page cannot submit or cancel Runs;
the host path has mock coverage but no live API integration yet. See [its
boundary and checks](docs/development/ui-preview-and-cli-gates.md).

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
