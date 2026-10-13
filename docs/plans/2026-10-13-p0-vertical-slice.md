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

**Partial result, 2026-10-13:** Host adapters and separate successful no-tools Claude and explicit-path Codex calls are implemented. The provisional API/PostgreSQL Compose slice reaches readiness and handles authenticated, idempotent task intake; a queued Run survived an API restart and a normal Compose group stop/start. Queue claim, lease renewal, cancellation, conditional completion, durable claim/completion/quarantine journal and no-replay quarantine have isolated live tests. Windows Job Object containment passed live child, breakaway-attempt and disposable host-exit tests. An opt-in Compose worker completed one synthetic Run in a dedicated database. A separate one-shot host worker produced a passing sample diff through queued Codex execution; a continuation Run reused that exact diff, passed both suites, obtained a structured Claude approval and stored a local commit. A persistent synthetic daemon subsequently passed polling and controlled crash/lease quarantine tests in a separate test database. Scoped host HTTP transport is implemented and tested with dummy credentials, but has not been granted or deployed to core. The complete SPEC core group and full CLI recovery remain open. See [earlier measurements](../experiments/2026-10-13-flow-cli-and-api.md), [recovery/code evidence](../experiments/2026-10-13-p0-recovery-and-code.md) and [daemon/transport evidence](../experiments/2026-10-13-worker-transport-and-daemon.md). This milestone is open.

### Remaining P0 work

1. [x] Preserve a queued sample diff, acceptance results, structured cross-provider review and local commit with source-Run provenance. This used an explicitly labeled continuation Run, not a full autonomous correction loop in one Run.
2. [x] Test controlled Windows runtime-host exit and a breakaway request with only fixture processes; test durable lease/journal and no replay after a test worker exits abruptly. These observations define a supported, narrow process mode, not universal isolation.
3. [x] Run a Compose worker against an isolated PostgreSQL queue and synthetic runtime; keep the shared CAF queue empty.
4. [ ] Complete the host transport boundary. An exact, expiring one-Run API grant and child-environment filtering have dummy-token and isolated SQL tests; a persistent synthetic daemon passed separate database tests. An approved temporary host loopback HTTP check passed for one synthetic Run, including claim/ACK, foreign-Run denial and revocation; see [evidence](../experiments/2026-10-13-scoped-http-procedure.md#measured-result-2026-10-13). Exact host workspace mapping and a private worktree root pass [offline checks](../experiments/2026-10-13-offline-workspace-and-recovery.md). A further approved [PostgreSQL and HTTP crash/restart check](../experiments/2026-10-13-postgres-http-crash-restart.md) passed with one disposable child, real lease expiry, durable quarantine and no replay. Provider login with the filtered environment and real CLI crash behavior remain unverified. Connect an always-on real worker to `core` only after separate boundary tests and approval.
5. [ ] Run actual CrewAI Flow plan → Codex implementation → Claude review → bounded Codex correction → tests in one durable Run, with a negative-review case and repeatable restart/cancel behavior.
6. [ ] Extend and test the complete `core` group and optional-group status/log commands; keep unrelated containers and shared dependencies safe. Redis remains a design decision because PostgreSQL currently holds queued Runs.
7. [ ] Persist the remaining SPEC events, checkpoints, findings, gate results and metrics, then run comparable A/B/C experiments on identical inputs. Verify Mode A's manager backend and separate API-model cost.

A [UI inspection workbench](../development/ui-preview-and-cli-gates.md) covers
task-body validation and local Run inspection. An optional host-only server
uses an existing API bearer to read one configured Run's status, typed results
and lease journal. This is mock-tested, not live-verified against PostgreSQL,
and offers no human identity auth, full events or service controls. The
[consolidated live gates](p0-live-gates.md) include filtered-environment CLI
checks, real provider execution and real CLI recovery; these remain open.

## Milestone 3: comparable experiment

Execution: after shared schema and gates are stable. Run Modes A, B and C on identical sample commit/task/limits. Verify CrewAI manager/backend requirements, separate model API cost from CLI usage, record outcomes and write a verdict under `docs/experiments/`. Later P2–P4 remain governed by [scope](../requirements/scope.md).

## Verified environment facts and open assumptions

See [environment](../development/environment.md). The user authorized push and development. Available CLI authentication does not prove CLI operation inside Docker or CrewAI Mode A subscription-only execution. Those remain tests/decisions.
