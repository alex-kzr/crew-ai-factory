# Local deployment and operations

Source: [SPEC §§5-6, 12, 15-16](../../SPEC.md). Target: Windows 11 with WSL2 and Docker Desktop.

## Current runnable scope

The Compose file at [`infrastructure/compose/compose.yaml`](../../infrastructure/compose/compose.yaml) defines one project named `caf` and one `core` profile containing **PostgreSQL and control-api only**. The API image uses the child repository's Dockerfile; its startup command migrates the P0 schema and starts Uvicorn. PostgreSQL has no published port. The API publishes container port 8000 on host `127.0.0.1:8123` by default; set `CAF_API_PORT` to choose another host port. Both services have readiness health checks and share the private `caf` network. Database data persists in the Compose-managed `caf_postgres_data` volume. `down core` stops the two containers without removing data.

**Verification:** `docker compose config --quiet` and the wrapper's Bash syntax/help/config commands passed on 2026-10-13. Containers have **not** been started by this change, so startup, health, migrations and Docker image builds are not yet verified. The `core` profile is a provisional API/database slice, **not** the complete SPEC core group. The worker has no daemon; agent-runtime has no verified CLI/host integration. Redis is not used by this slice. `ui`, `observability`, `dev` and `all` deliberately return unavailable from the wrapper rather than starting a partial stack.

## Credentials and first startup

Use an initialized recursive checkout. Supply credentials in your local shell environment; never put them in Git. `CAF_API_TOKEN` needs at least 32 characters. `CAF_POSTGRES_PASSWORD` needs at least 16 URL-safe characters from letters, digits, `.`, `_`, `~`, `-`; this restriction keeps the generated PostgreSQL URL unambiguous. Do not paste real values into tickets or logs. Example PowerShell setup with locally generated values:

```powershell
$env:CAF_API_TOKEN = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
$env:CAF_POSTGRES_PASSWORD = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(24))
$env:CAF_API_PORT = '8123'
```

Run the wrapper from the umbrella root in WSL or Git Bash after the API Dockerfile and image build have been checked:

```sh
bash scripts/services.sh config
bash scripts/services.sh build core
bash scripts/services.sh up core
bash scripts/services.sh status
bash scripts/services.sh logs core
bash scripts/services.sh down core
```

`config` uses `docker compose config --no-interpolate` so it does not expand credentials in terminal output. `up core` validates credentials, builds and starts just `control-api` and `postgres`, and waits for their health checks. `build core` builds only the API image. `status`/`ps` and `logs core` inspect only Compose project `caf`; `logs control-api` and `logs postgres` select one service. `down core` uses `stop` on those exact services; it never runs project-wide `down` or removes volumes. No cleanup command that deletes data is provided. Keep the project name `caf` reserved for this project.

The API health endpoints are `/health/live` and `/health/ready`; readiness checks a connection to the migrated `runs` table. With the default host port, local clients use `http://127.0.0.1:8123`. The API requires `CAF_API_TOKEN` for execution endpoints. Docker operators can inspect container environment, so the local Docker account must be trusted. There are no host-home, CLI-auth, Docker-socket or runtime-worktree mounts.

## Future group behavior

SPEC `core` ultimately includes orchestration-worker, runtime integration and essential stores. Add a worker only after a tested long-lived daemon and readiness contract exist. Add Redis only if the chosen coordination path uses it. [Compose profiles](https://docs.docker.com/compose/how-tos/profiles/) select containers, not lifecycle ownership: before enabling optional groups that share PostgreSQL, update `down core` to detect and preserve active dependents. Until then the wrapper rejects the optional groups. A host-executed runtime must be shown as a host process in status, never as a Docker container.

Development overrides/hot reload, resource tuning, observed startup behavior, failure recovery and safe cleanup procedures remain pending. See [verification](../development/verification.md) and [the P0 plan](../plans/2026-10-13-p0-vertical-slice.md).
