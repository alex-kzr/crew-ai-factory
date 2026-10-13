# Local deployment and operations design

Source: [SPEC §§5–6, 12, 15–16](../../SPEC.md). Target: Windows 11, WSL2 and Docker Desktop. **No Compose files, commands or services are runnable yet.** This page is the implementation contract for the next slice.

## Group model

Use Docker Compose `profiles` for actual container selection and a tested `scripts/services.sh` wrapper for human-friendly groups. `core` includes API, worker, Postgres, Redis and runtime integration. `ui` adds web UI and dependencies; `observability` adds optional telemetry; `dev` adds local utilities; `all` selects all appropriate profiles. Base stores needed by active groups must be started as dependencies. If runtime executes on WSL host, status and readiness must identify it as a host process, never a Docker service.

The wrapper must implement and test `up core`, `up ui`, `up all`, `down core`, `status`, and `logs <service-or-group>`, plus document `config`, `build`, `ps` and safe cleanup. `down core` must not remove stores still needed by UI or observability; track active group ownership or reject unsafe partial stops. Compose profile selection alone does not give this behavior. If `configs/service-groups.yaml` is introduced, validate its service names against rendered Compose config.

Implement health checks and health-conditioned dependencies as appropriate; running is not ready. Document ports, local volumes, isolated networks, resource budgets, restart policy, environment variables and dev hot reload overrides. Do not put credentials in Compose files or broad host-home mounts. Keep persistent volumes when stopping a group; deletion must require an explicit cleanup command.

## Runtime location decision

Either Docker with narrow workspace/auth mounts and demonstrated CLI auth or a WSL host runtime behind the same service boundary. Verify Git/filesystem/CLI versions, auth availability, cancellation and process-tree behavior before choosing. See [ADR 0001](../architecture/decisions/0001-repository-and-runtime.md).

## Bootstrap today

Local submodule checkouts already exist; on another machine `git submodule update --init --recursive` will fail until child remotes are published and `.gitmodules` is updated. The umbrella bootstrap command and Compose wrapper are pending implementation. See [repository publication](../development/repositories.md). No runtime command should be inferred from this design page.
