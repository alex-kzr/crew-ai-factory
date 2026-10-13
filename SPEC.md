# CAF - CrewAI Factory: Build an CrewAI Code Factory

## 1. Mission

Design and implement a **new, independent experimental project** to evaluate CrewAI as the orchestrator of an autonomous software development factory. The factory must coordinate **Codex CLI** and **Claude Code** as external, fully capable coding agents, rather than replacing their internal agent loops with plain LLM API calls.

The project must use an **umbrella repository** containing documentation and independently managed application/service repositories. Its runtime architecture must be **Docker-based microservices**, with explicit **service groups** that can be started, stopped, and observed together.

This is a greenfield experiment, **not an extension or migration of any existing AI factory**. Make architectural decisions testable; avoid presenting unverified CrewAI/CLI capabilities as established facts.

## 2. Goals and evaluation questions

Implement and evaluate:

1. Role-based agent collaboration: lead/planner, developer, reviewer, QA.
2. Codex CLI and Claude Code integration through a provider-neutral runtime adapter.
3. CrewAI Crews and Flows, including delegation, task dependencies, branching, retries, and execution state.
4. Parallel development using isolated Git worktrees and independent branches.
5. Review → correction → retest loops with configurable limits and quality gates.
6. Cancellation, timeouts, crash recovery, session resume where supported, and durable audit trails.
7. Microservice deployment with Docker Compose service profiles/groups and minimal startup modes.
8. Comparison against a baseline Python orchestrator to determine whether CrewAI provides measurable value.

**Primary research question:** Does CrewAI usefully orchestrate autonomous Codex/Claude coding agents, or does the integration require a custom orchestration layer that makes CrewAI redundant?

## 3. Non-goals for the initial implementation

- Kubernetes, production multi-tenancy, SaaS billing, and enterprise IAM.
- Building a generic replacement for Codex CLI or Claude Code.
- Requiring LLM API keys for coding execution when authenticated CLI workflows suffice.
- Introducing Temporal, RAG, vector databases, or a message broker other than Redis without demonstrated need.
- Assuming Git worktrees provide process or security isolation.

## 4. Umbrella repository structure

The top-level repository is the **umbrella repository**. It tracks architecture, documentation, deployment manifests, environment examples, tooling, and integration tests. It must not absorb the source history of independently developed applications/services.

```text
crewai-code-factory/                  # umbrella Git repository
├── README.md
├── AGENTS.md                          # instructions for coding agents
├── docs/                              # all project documentation
│   ├── README.md
│   ├── requirements/
│   ├── architecture/
│   │   ├── overview.md
│   │   ├── services.md
│   │   ├── runtime-adapters.md
│   │   ├── workflow.md
│   │   └── decisions/                 # ADRs
│   ├── development/
│   ├── operations/
│   ├── experiments/
│   └── api/
├── repositories/                      # independent application/service Git repos
│   ├── control-api/
│   ├── orchestration-worker/
│   ├── agent-runtime/
│   ├── web-ui/
│   └── sample-app/                    # coding target for experiments
├── infrastructure/
│   ├── compose/
│   │   ├── compose.yaml
│   │   └── compose.dev.yaml
│   ├── docker/
│   └── observability/
├── configs/
│   ├── agents/
│   ├── workflows/
│   └── service-groups.yaml
├── scripts/
│   ├── bootstrap.sh
│   ├── services.sh
│   └── doctor.sh
├── tests/
│   └── integration/
├── .env.example
└── .gitignore
```

### Repository ownership and initialization

- Each directory in `repositories/` represents an independently versioned Git repository with its own README, tests, package/dependency definitions, and CI configuration as appropriate.
- Use **Git submodules** for reproducible umbrella checkouts, unless an ADR documents a stronger reason for a different approach. Record pinned commits in the umbrella repository.
- Provide `scripts/bootstrap.sh` (or an equivalent `make bootstrap`/task runner entry) that initializes submodules and sets up the developer environment.
- Do not commit credentials, `.env`, CLI authentication data, generated worktrees, build outputs, or runtime state.
- Runtime task worktrees must be created **outside** tracked submodule working directories, for example under `${FACTORY_WORKSPACE_ROOT}/runs/<run-id>/<task-id>/`.
- Document how to update submodule versions and how to create a new application/service repository.

## 5. Microservice boundaries

Use small, explicit service contracts. Start with the following logical services:

| Service | Responsibility | Proposed stack |
|---|---|---|
| `control-api` | Projects, tasks, runs, agent configuration, events and streaming API | Python, FastAPI, Pydantic |
| `orchestration-worker` | CrewAI Flows/Crews, task dispatch, state transitions, quality-gate workflow | Python, CrewAI |
| `agent-runtime` | Execute/monitor/cancel Codex and Claude CLI processes, allocate workspaces, collect structured events | Python, asyncio, subprocess |
| `web-ui` | Configure experiments, submit tasks, inspect graphs/logs/results and service states | React, TypeScript, Vite, TanStack Query |
| `postgres` | Durable run/task/event metadata, checkpoints and configuration | PostgreSQL |
| `redis` | Queue/coordination and temporary runtime state | Redis; ARQ only if justified |
| `observability` (optional) | Traces, log correlation, evaluations and dashboards | OpenTelemetry, Langfuse as candidate |

**Separation rule:** CrewAI owns the agent/workflow orchestration experiment; the runtime service owns external CLI execution. The API does not directly run long-lived coding processes.

**Important execution constraint:** Codex and Claude CLI need an appropriate filesystem, Git installation, working directory, and secure access to their authentication context. Decide whether the `agent-runtime` runs in a Docker container with explicitly mounted workspaces and credentials, or on the WSL host while the other services run in Docker. **Implement and document a verified approach**, including its threat model. Do not assume user CLI subscription credentials work automatically inside containers. Keep this service a clear boundary even if its first implementation is a WSL-host process.

## 6. Docker Compose and service grouping

All containerized infrastructure/services must be defined and runnable with **Docker Compose**, targeting **Windows 11 + WSL2 + Docker Desktop** as the primary local environment.

Implement named **startup groups** using Compose `profiles`, with a small wrapper script providing human-friendly operations. Distinguish deployment/service profiles from CrewAI agent roles.

Suggested groups:

| Group | Contents | Purpose |
|---|---|---|
| `core` | `control-api`, `orchestration-worker`, essential stores, runtime integration | Minimal headless experiment |
| `ui` | `web-ui` | Visual management |
| `observability` | tracing, log/telemetry UI and collectors | Inspect behavior and failures |
| `dev` | dev-only utilities and debugging tools | Local development |
| `all` | All appropriate services | Full local stack |

Requirements:

- Implement **real, tested commands** such as `./scripts/services.sh up core`, `up ui`, `up all`, `down core`, `status`, and `logs <service-or-group>`. The wrapper may select Compose profiles and dependencies; do not invent unsupported native Compose group behavior.
- Define which foundational services are always started as dependencies (e.g., database and Redis) and how groups overlap.
- Use health checks and `depends_on` health conditions where appropriate; do not treat container started as application ready.
- Keep local persistent volumes, isolated networks where useful, environment variables, resource limits, predictable ports, and restart behavior explicit.
- Support development overrides/hot reload without changing the production-like baseline compose file.
- Document the behavior of stopping one group while shared dependencies are used by another group; avoid accidental shutdown of in-use shared services.
- Document commands for `config`, `build`, `up`, `down`, `ps`, `logs`, and safe cleanup.
- If agent-runtime is host-executed, display it in group status and expose readiness/health consistently; do not misleadingly claim it is a Docker service.
- `configs/service-groups.yaml` (if used) is the declarative source for human-friendly groups; validate it against real Compose service names. Compose profiles are the actual container selection mechanism.

## 7. CrewAI integration experiments

Implement three comparable execution modes sharing the same task schemas, CLI adapters, Git/workspace manager, test runner and evaluation criteria:

- **Mode A — Crew-as-Tool:** CrewAI Agents delegate CLI coding tasks through custom CrewAI tools. Verify how the manager LLM is configured; separate any model API costs from CLI subscription-based execution.
- **Mode B — Flow-to-CLI:** A CrewAI Flow invokes independent Codex/Claude runtime adapters directly, retaining each CLI's native internal tool/agent loop.
- **Mode C — Baseline:** An equivalent plain Python `asyncio` workflow without CrewAI, for controlled comparison.

Do not describe A as subscription-only unless empirically verified. Document CrewAI framework version, model backend configuration, auth and limitations per mode.

Run each mode on the same benchmark tasks with reproducible starting repository commits.

## 8. Agent roles and configurable team

Default roles:

- **Tech Lead / Planner (Claude):** define tasks, dependencies and acceptance criteria.
- **Developer (Codex):** implement source changes and tests in an assigned worktree.
- **Reviewer (Claude):** review actual diffs, report actionable findings and acceptance verdict.
- **QA (Codex):** create/run targeted tests and report reproducible failures.

Store team definitions in version-controlled configuration. Allow changing the CLI provider/model/configuration per role; do not hard-code the role-to-provider mapping. Capture the distinction between **CrewAI Agent** and **external coding agent** in schema and UI.

## 9. External agent runtime contract

Introduce typed models and a unified interface, for example:

```python
class CodingAgentRuntime(Protocol):
    async def execute(
        self,
        task: CodingTask,
        workspace: Path,
        session_id: str | None = None,
    ) -> AgentResult: ...

    async def cancel(self, run_id: str) -> None: ...
    async def get_status(self, run_id: str) -> AgentStatus: ...
```

Implement `CodexRuntime` and `ClaudeRuntime` with:

- Verified non-interactive CLI invocation flags for the installed versions.
- Incremental parsing of structured JSON/JSONL events where supported.
- Session identifiers and resume when verified by tests.
- Explicit working directory, allowed tool/sandbox permissions, timeouts and cancellation with child-process cleanup.
- Stdout/stderr retention with secret redaction, correlation IDs and reproducible invocation metadata.
- Structured results containing changed files, commits/diff, exit status, error details and available usage metrics.
- Securely stored or mounted CLI authentication; never log tokens or credentials.

Do not build commands through a shell with untrusted interpolation. Distinguish infrastructure failures, agent failures, timeouts, and quality-gate failures.

## 10. Development workflow and Git isolation

Default lifecycle:

1. User creates a coding task with target repo, base revision, constraints and acceptance criteria.
2. Planner generates a structured plan and task dependency DAG.
3. Scheduler prepares a branch and worktree for each runnable task.
4. Codex and/or Claude coding agents execute independent tasks in parallel where dependencies permit.
5. Integration stage merges/cherry-picks changes into a dedicated integration branch; failures/conflicts become explicit tasks.
6. Reviewer inspects the **integrated diff**.
7. QA and deterministic quality gates run against the **integrated tree**.
8. Failed reviews/tests trigger bounded correction loops; repeated failure becomes `blocked`.
9. Successful run records commits, artifacts and final summary. Do not automatically push, open PRs or merge into the protected main branch without a configurable approval policy.

A worktree is Git isolation, **not security isolation**. Specify filesystem, network, process and secret access restrictions for untrusted code execution. Use sandboxed execution as an explicit capability; document any limits of the MVP.

## 11. Persistent data and telemetry

Track at least `Project`, `Repository`, `AgentProfile`, `Task`, `TaskDependency`, `Run`, `RunStep`, `AgentSession`, `Workspace`, `Artifact`, `Event`, `ReviewFinding` and `QualityGateResult`.

Maintain stable identifiers and correlation IDs across API, orchestration, runtime and logs. Preserve append-only events or equivalent auditable history of state transitions. Persist enough state to recover after a worker restart, and **test recovery rather than assuming CrewAI supports it automatically**.

Capture: total elapsed time, per-stage timing, iterations, completion status, tests passed/failed, CLI exit reasons, interruptions, successful resumes, approximate token/usage data when emitted, and API-model costs separately from subscription CLI usage.

## 12. Security and operational requirements

- Protect execution endpoints; even a local-only setup must not expose arbitrary command execution on public interfaces.
- Keep secrets out of Git and logs; document a minimal local credentials workflow.
- Limit concurrency, retries, wall time, CPU/memory and workspace disk consumption.
- No automatic elevated permissions; sandbox mode and approval policy must be explicit.
- Add process cleanup, orphan-worktree reconciliation, idempotent task start and graceful shutdown.
- Test service readiness and failure behavior when Docker, Redis, Postgres or either CLI is unavailable.
- Document risks of mounting Docker socket, host home folders, or authentication directories; avoid broad mounts by default.

## 13. Recommended technology choices

- Python 3.12+ and **uv** for all Python services.
- CrewAI pinned to a tested version; FastAPI + Pydantic v2.
- Python `asyncio` + safe subprocess APIs for CLI workers.
- Git worktrees and native Git CLI.
- PostgreSQL for durable records; Redis for coordination/queue where needed.
- React + TypeScript + Vite, TanStack Query for the UI.
- pytest, pytest-asyncio, typed Python and static checks.
- OpenTelemetry with optional Langfuse integration after core scenarios work.
- Docker Compose with named service profiles and the service group wrapper.

Do not add Temporal or Kubernetes to the MVP. Document any deviations through ADRs.

## 14. Delivery phases

### P0 — Umbrella scaffold and end-to-end proof of concept

- Create the umbrella Git repository layout, docs, AGENTS.md, bootstrap tool and independently initialized service repositories.
- Set up uv projects and a minimal Compose deployment with verified service groups.
- Implement Codex/Claude adapters with one verified command path each.
- Build a CrewAI Flow that runs: plan → Codex implementation → Claude review → Codex correction (if needed) → tests.
- Produce commits, logs and structured artifacts from a sample application.
- CLI execution, repo isolation and credential mounting must be documented and tested.

### P1 — CrewAI comparative evaluation

- Implement Mode A, Mode B and Mode C with equivalent fixtures.
- Run benchmarks and write findings in `docs/experiments/`.
- Verify hierarchical delegation and assess any separate LLM/API-key requirement.

### P2 — Parallel coding

- Task DAG, parallel worktrees, integration branch, conflicts, gating and concurrency limits.

### P3 — Reliability

- Persistent run state, queue/coordination, recovery tests, cancellation, observability and audit trail.

### P4 — UI

- Task intake, team editing, workflow/run visualization, live event stream, artifact browsing, grouped service status/control.

Complete working vertical slices; do not implement a large skeleton with placeholder services that cannot run.

## 15. Required deliverables

1. Runnable umbrella repository with initialized child repositories and documented bootstrap.
2. Architecture documents, service diagram, data-flow diagram, ADRs and service contracts in `docs/`.
3. Docker Compose configuration and tested group-management commands.
4. Functioning Codex/Claude runtime adapters with automated tests.
5. Executable CrewAI Flow/Crew examples and baseline orchestrator.
6. At least one runnable sample repository and reproducible development task fixture.
7. E2E test proving a coding change, review, test and persisted artifact.
8. Experiment report with results, tradeoffs, known limitations and recommendation on CrewAI's suitability.
9. Setup/run/troubleshooting documentation for WSL2 + Docker Desktop.

## 16. Acceptance criteria

The assignment is accepted when:

- A fresh developer checkout can bootstrap all tracked child repositories and bring up the **core** service group through one documented command sequence.
- Starting the **ui** or **observability** group enables only the requested optional components and their necessary dependencies; status/logs work by group.
- A task submitted to the system causes an authenticated Codex or Claude CLI instance to change a target Git repository in a dedicated worktree.
- The other coding agent can review the integrated code and submit structured feedback.
- At least one negative review or failing test causes bounded rework and reevaluation.
- A successful run contains the Git commit(s), test results, review findings, timestamps and traceable logs.
- Two independent implementation tasks can run concurrently without sharing a writable worktree.
- Cancelling a running task terminates the CLI process tree and records the outcome.
- Restart/recovery behavior is demonstrated and documented with any known limitations.
- Modes A/B/C are compared using identical fixtures and a written experimental verdict.
- No secrets, credentials or generated runtime workspaces are committed into source control.

## 17. Instructions to the implementing agent

Begin by inspecting the environment and verifying available versions and authentication state of CrewAI, Codex CLI, Claude Code, Git, Docker Compose and uv. Record verified facts and assumptions separately. Then produce a concise implementation plan and start with P0 without waiting for unnecessary approvals. Use working code and tests, not architectural stubs. Prefer simple, documented interfaces. If a proposed CLI capability or CrewAI integration is unsupported, demonstrate the limitation, choose the smallest viable alternative and document the architectural impact. Keep documentation in English and update it alongside each implementation increment.
