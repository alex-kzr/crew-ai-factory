# P0: synthetic vertical slice and verified integration

Date: 2026-10-13. Source: [SPEC §§4–10, 14–16](../../SPEC.md). This plan starts implementation; passing its first milestone is not completion of SPEC P0 or system acceptance.

## Milestone 1: deterministic, credential-free contract — verified 2026-10-13

Execution: [parallel: P0S-01, P0S-02, P0S-03], followed by [same-session: P0S-04].

- [P0S-01](tasks/P0S-01_runtime-contract.md): provider-neutral runtime protocol and synthetic adapter, typed events/results, cancellation and failure tests.
- [P0S-02](tasks/P0S-02_sample-fixture.md): runnable sample app plus reproducible coding task fixture and tests.
- [P0S-03](tasks/P0S-03_orchestration-loop.md): synthetic plan → implementation → review → bounded correction → tests; baseline mode and, only if verified without paid model access, CrewAI Flow mode.
- [P0S-04](tasks/P0S-04_integration.md): integrate pinned child commits, run shared contract/E2E checks, capture artifacts and compare intended versus observed behavior.

**Done when:** a fresh checkout bootstraps submodules; synthetic run starts from a recorded fixture commit, emits traceable structured steps, exercises a negative review or failing test and bounded correction, executes deterministic tests, stores a final artifact, and the same fixture is runnable in the available modes. Findings and unavailable modes are documented honestly. No real CLI credentials are needed for this gate. This gate passed from a fresh recursive clone at umbrella commit `231d0a4`; see [evidence](../experiments/2026-10-13-synthetic-baseline.md).

## Milestone 2: actual CLI and core services

Execution: same-session after Milestone 1. Verify Codex/Claude non-interactive flags and one safe invocation each using existing CLI profiles, then build a small real API/worker/runtime/Redis/Postgres slice. Use one Docker Compose **project** named `caf`, with named profiles/groups and one `scripts/services.sh` entrypoint; do not touch other projects' containers, ports, volumes or data. Decide runtime host/container location through a tested threat model. Test `core` startup, readiness, cancellation, persistence and restart recovery. Do not add a paid model/API fallback or new credential workflow without user decision.

**Partial result, 2026-10-13:** Host adapters and separate successful no-tools Claude and explicit-path Codex calls are implemented. An earlier unqualified Codex call selected a different installed version and failed; the cause was not established. The provisional API/PostgreSQL Compose slice reaches readiness and handles authenticated, idempotent task intake; a queued Run survived an API container restart and a normal Compose `down core`/`up core`. PostgreSQL queue claim, owner-guarded lease renewal and completion have isolated live tests. A test-only worker bridge claimed one Run in a dedicated database, executed only the synthetic runtime and persisted a labeled artifact. No CLI source edit or cross-provider review has run. The worker is not a daemon, so the complete SPEC core group and worker recovery remain open. See the [measured follow-up](../experiments/2026-10-13-flow-cli-and-api.md). This milestone is open.

### Remaining P0 work

1. Verify a real code-changing Codex run and Claude review on the same disposable fixture, revision, permissions and deterministic test gate. This needs a separately authorized code-changing CLI task.
2. Add a bounded worker process for the shared queue, repository and revision verification, isolated worktrees, real runtime calls, cancellation, lease heartbeat and reconciliation of interrupted CLI processes before any expired Run is reclaimed.
3. Extend the Compose `core` group beyond the tested API/PostgreSQL slice only as those components become runnable; test readiness, shutdown, persistence and restart recovery. Redis integration remains a design decision for the first durable queue because PostgreSQL currently holds queued Runs.
4. Persist the remaining events, checkpoints, findings, gate results and metrics required by SPEC, then run comparable A/B/C experiments with identical fixture, controls and measured cost. Mode A's model backend and subscription assumptions need verification.

## Milestone 3: comparable experiment

Execution: after shared schema and gates are stable. Run Modes A, B and C on identical sample commit/task/limits. Verify CrewAI manager/backend requirements, separate model API cost from CLI usage, record outcomes and write a verdict under `docs/experiments/`. Later P2–P4 remain governed by [scope](../requirements/scope.md).

## Verified environment facts and open assumptions

See [environment](../development/environment.md). The user authorized push and development. Available CLI authentication does not prove CLI operation inside Docker or CrewAI Mode A subscription-only execution. Those remain tests/decisions.
