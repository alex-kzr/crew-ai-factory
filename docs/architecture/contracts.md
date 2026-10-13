# Data and interaction contracts

Source: [SPEC sections 7-11](../../SPEC.md). Most of this page remains a **target contract outline**. The [control API P0 schema and worker handoff](../../repositories/caf-control-api/docs/worker-contract.md) implement Task and Run intake/status plus conditional queue claim, lease renewal, cancellation, completion and expired-Run quarantine. The isolated [worker proof](../../repositories/caf-orchestration-worker/README.md#explicit-queue-to-synthetic-proof) exercises the synthetic runtime in a dedicated test database, and a separate [dispatch boundary](../../repositories/caf-orchestration-worker/README.md#lease-aware-dispatch-boundary) exercises one lease-aware claim/ACK. They do not fulfill the full entity, transport, checkpoint or audit requirements below.

## Stable identity and durable records

Minimum entities: `Project`, `Repository`, `AgentProfile`, `Task`, `TaskDependency`, `Run`, `RunStep`, `AgentSession`, `Workspace`, `Artifact`, `Event`, `ReviewFinding`, `QualityGateResult`. Use stable IDs and propagate a correlation ID through API requests, queue messages, worker, runtime and logs. Persist state transitions in append-only events or an equivalent audit history, and enough checkpoints to prove worker restart recovery. Redis is not the only copy of durable state.

| Record | Core relationships / required information |
|---|---|
| Project, Repository | Project targets repositories and immutable base revisions |
| AgentProfile | Role, CLI provider/model/config, permissions; distinguish CrewAI Agent from external coding agent |
| Task, TaskDependency | Task input/acceptance, target revision, DAG edges |
| Run, RunStep | Mode, status, timing, iteration, failure class, checkpoint |
| AgentSession, Workspace | CLI session/resume metadata if verified; worktree/branch/commit identity and cleanup state |
| Artifact, Event | Artifact location/checksum, ordered timestamped state and CLI events with correlation ID |
| ReviewFinding, QualityGateResult | Diff location, finding/verdict, command, exit status and evidence |

**Proposed interaction sequence:** API validates and persists a run request, coordination wakes worker, worker issues a typed runtime task, runtime emits incremental events and returns a terminal result, worker integrates and gates the code, then records final artifacts. The implemented P0 API exposes authenticated `POST /v1/tasks`, `GET /v1/runs/{id}` and `POST /v1/runs/{id}/cancel` and atomically stores Task plus queued Run. The [worker claim/completion contract](../../repositories/caf-control-api/docs/worker-contract.md) implements transactional claim and conditional completion; test-only worker functions exercise the handoff. There is no polling daemon, automatic wake-up, safe expired-lease replay or production runtime integration. Event delivery and ordering guarantees are **decision pending**.

## Runtime adapter boundary

`execute(task, workspace, session_id?) -> AgentResult`, `cancel(run_id)`, `get_status(run_id)` are the SPEC's conceptual operations. Results must distinguish infrastructure, agent, timeout and quality-gate failures; include exit reason, changed files, diff/commits, error detail and usage when emitted. Stream structured JSON/JSONL where supported, retain redacted stdout/stderr, and track invocation metadata without tokens. CLI flags and resume behavior must be verified against installed versions. Use subprocess argument arrays, explicit cwd, permissions and process-tree cleanup.

## Metrics and comparison

For every mode/fixture, collect elapsed and per-stage time, iteration count, completion state, passed/failed tests, CLI exits, interruptions/resumes, approximate usage if emitted, and separate model API cost. Starting commit, task prompt, gate commands, permissions and time limits must match across modes. Undefined or unavailable usage is recorded as unavailable, not zero.
