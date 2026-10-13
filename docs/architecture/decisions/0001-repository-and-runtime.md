# ADR 0001: Repository topology and runtime location

Status: **partial decision; execution location pending**  
Source: [SPEC §§4–6, 9, 12–13](../../../SPEC.md)

## Decision: repository topology

The umbrella owns docs, eventual deployment/config/scripts/integration tests and pins five independently managed repositories as Git submodules: `control-api`, `orchestration-worker`, `agent-runtime`, `web-ui`, `sample-app`. PostgreSQL, Redis and optional observability use infrastructure images/config rather than extra application repositories. This matches the logical ownership boundaries in SPEC §5 without splitting every dependency into a separate source repository.

Each child currently has a local initial commit and a README only. No dependency manifest, CI or tests are added until executable code has a concrete contract. Local submodule URLs are temporary and non-portable; [publication steps](../../development/repositories.md) are required before a remote umbrella checkout works.

## Decision pending: execution location

The runtime must remain a separate contract, but its first process location is undecided. Compare (a) a container with narrow worktree/auth mounts and verified CLI subscription behavior, and (b) a WSL host process with a private authenticated interface to container services. Record threat model, CLI versions/auth availability, process cleanup and readiness evidence. Do not present either as implemented.

## Other open questions

- Exact CLI flags, structured event formats and resume support for the installed versions.
- CrewAI version, manager LLM backend, API key/cost requirements in Mode A, and state recovery guarantees.
- Queue/transport and exact API/event schemas; checkpoint and event ordering semantics.
- Safe partial group stop behavior when services share stores.
- Sandbox policy for untrusted code, network access and mounted credential scopes.
- Benchmark tasks, scoring and acceptable confidence for the A/B/C verdict.

Resolve these through small recorded tests and follow-up ADRs before turning proposals into commitments.
