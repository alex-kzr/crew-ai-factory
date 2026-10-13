# Security, tests and acceptance

Source: [SPEC sections 9-12 and 15-16](../../SPEC.md). Checks below are target acceptance layers. Synthetic contract/worktree and Flow parity tests, API route tests, separate Codex and Claude no-tools CLI smoke calls, and live API/PostgreSQL Compose readiness and task intake have passed. A queued Run remained readable after an API container restart. Queue claim/cancel/completion, a transactionally persisted lifecycle journal, crash quarantine and a Compose synthetic worker passed isolated live PostgreSQL tests. Windows Job Object containment passed live local-process tests, including disposable host exit and a contained breakaway request; unverified cleanup leaves a queue claim unacknowledged. A fixture-specific queued Codex diff, deterministic gates, source-linked Claude approval and local commit are stored as durable test Run artifacts. A production worker daemon, secure shared-queue runtime boundary, complete real CrewAI Flow and actual mode comparison remain pending. See [earlier follow-up](../experiments/2026-10-13-flow-cli-and-api.md) and [new evidence](../experiments/2026-10-13-p0-recovery-and-code.md).

## Security boundaries

- Authenticate and authorize execution endpoints; bind local services privately by default.
- No tokens, CLI auth, `.env`, generated worktrees or runtime logs in Git. Redact captured streams and keep credentials in a narrow local workflow.
- Set explicit filesystem, network, process and secret access for untrusted code. Git worktrees isolate changes, not process behavior.
- Set concurrency, retry, wall-time, CPU/memory and disk limits. No automatic elevated permissions.
- Avoid Docker socket and broad home/auth mounts by default. Document any exception and its threat model.
- Use argument-array subprocess calls with cwd and environment allowlist. Test cancellation and child cleanup, orphan reconciliation, idempotent starts and graceful shutdown.

## Verification ladder

1. **Contracts/unit:** validation, state transitions, DAG, adapter event parsing/redaction, failure classification, gate policy and retry limits.
2. **Runtime integration:** real installed Codex/Claude non-interactive invocation on disposable sample repo, permissions, timeout, cancel/process tree, session resume only if supported, and missing CLI/auth failures.
3. **Services:** Compose config/profile selection, readiness, dependency failure, group overlap/stop semantics and optional status/logs.
4. **E2E:** task intake → dedicated worktree → coding commit → integrated review → negative finding or failing test → bounded rework → passing tests → persisted findings, timestamps, artifacts and traceable events.
5. **Reliability:** concurrent tasks never share writable worktree; worker restart/recovery; unavailable Docker, Postgres, Redis or either CLI; orphan cleanup.
6. **Experiment:** identical fixtures and base commits for Modes A/B/C, measured duration/quality/iterations/failure and separate API cost, with written recommendation.

The complete acceptance list remains in [SPEC §16](../../SPEC.md); use its individual bullets as release gates. A fresh recursive checkout and the provisional API/PostgreSQL slice have been verified. The complete SPEC `core` group and system acceptance remain open.
