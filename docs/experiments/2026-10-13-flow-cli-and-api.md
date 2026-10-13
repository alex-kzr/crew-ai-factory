# P0 follow-up: Flow, host CLI and control API

Date: 2026-10-13. Scope: partial implementation evidence against [SPEC sections 6, 7, 9, 14 and 16](../../SPEC.md). The [synthetic worktree baseline](2026-10-13-synthetic-baseline.md) remains the only end-to-end code-change test.

## Measured results

| Slice | Evidence | Limit |
|---|---|---|
| Runtime contract and host adapters | `caf-agent-runtime` commit `1be45698ac9d36317d348d48b3c451521319e7f5`; 31 tests passed locally. A no-tools Claude Code 2.1.296 call with the existing profile exited 0, emitted structured events and returned the expected marker. | A read-only Codex call exited 1 with an authentication-category diagnostic despite `codex login status` reporting a login. Subsequent read-only checks found that PowerShell selected npm CLI 0.162.1 while Python subprocess selected version 0.147.0 from the desktop installation. The exact provider error was not retained; this mismatch is not proven to cause it. No credentials were changed. No CLI made a code change. Windows child cleanup after the parent exits is best effort, not verified. |
| CrewAI Flow Mode B | `caf-orchestration-worker` commit `ae7d38bcf6d9204834c784625eafc6f71e840120`; 17 tests passed with the pinned CrewAI 1.15.27 extra. Three scripted outcomes matched the asyncio baseline: correction success, exhausted review limit and test infrastructure failure. | Flow listeners call the same in-process synthetic runtime. No CrewAI Agent/manager LLM, router, durable state, CLI or network isolation claim was tested. Removing three common model-key variables in a test does not prove absence of all external traffic. |
| Control API | `caf-control-api` commit `2ff1ed1d486ee8047eb4214ada1d8d4772fd9f50`; 5 route tests, wheel build and Docker image build passed. Task intake requires a bearer token and writes Task plus queued Run in one PostgreSQL transaction by design. | Route tests use a fake store. A live PostgreSQL transaction, schema migration, image startup and worker claim/recovery remain untested. |
| Compose definition | `docker compose config --quiet`, selected service list (`postgres`, `control-api`), Bash syntax and wrapper help/config passed. | No container was started; startup, readiness, persistence and group stop behavior are unverified. The current `core` profile is only API and PostgreSQL. |

## Interpretation and next gate

The tested Flow can sequence the shared synthetic workflow without constructing a model-backed CrewAI Agent. It does not yet establish that CrewAI adds value for autonomous coding. The next meaningful comparison needs the **same starting sample commit, actual CLI tasks, Git integration, deterministic code tests, limits and artifact schema** in Modes B and C. Mode A needs a separately verified manager backend and cost record. [CrewAI's Flow reference](https://docs.crewai.com/en/concepts/flows) documents the listener mechanism used here; the [pinned package release](https://pypi.org/project/crewai/1.15.27/) identifies the tested version.

The current blocker for a Codex-backed code-change gate is the observed command-execution authentication failure. The API/database/worker boundary and Compose startup also need integration tests. Keep these as open checks rather than treating the passing synthetic tests as SPEC acceptance.
