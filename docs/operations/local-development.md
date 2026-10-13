# Local deployment and operations

Source: [SPEC §§5-6, 12, 15-16](../../SPEC.md). Target: Windows 11 with WSL2 and Docker Desktop.

## Current runnable scope

The Compose file at [`infrastructure/compose/compose.yaml`](../../infrastructure/compose/compose.yaml) defines one project named `caf` and one `core` profile containing **PostgreSQL and control-api only**. The API image uses the child repository's Dockerfile; its startup command migrates the P0 schema and starts Uvicorn. PostgreSQL has no published port. The API publishes container port 8000 on host `127.0.0.1:8123` by default; set `CAF_API_PORT` to choose another host port. Both services share the internal `caf_private` network; only the API also joins `caf_edge` so its loopback host port works. Both have readiness health checks. Database data persists in the Compose-managed `caf_postgres_data` volume. `down core` stops the two containers without removing data.

Core Compose does not pass through `CAF_WORKER_TOKEN` or any worker grant
settings. The published code for a scoped worker API is disabled there. The
next proposed HTTP check uses a separate temporary host API bound to loopback
and the isolated test database; see its [procedure]
(../experiments/2026-10-13-scoped-http-procedure.md). Do not set worker grant
variables or start a real CLI worker as part of ordinary `up core`.

**Verification:** `docker compose config --quiet` and the wrapper's Bash syntax/help/config commands passed on 2026-10-13. After Docker Desktop recovered, `up core` built the API image and both containers reached healthy. Host loopback liveness/readiness and live PostgreSQL task intake passed; see [measured results](#live-core-check-after-docker-recovery). The `core` profile is a provisional API/database slice, **not** the complete SPEC core group. The persistent daemon exists only in the separate synthetic test profile; core has no running worker. Redis is not used by this slice. `ui`, `observability`, `dev` and `all` deliberately return unavailable from the wrapper rather than starting a partial stack.

Opt-in experiment profiles are separate from `core`: `p0-test` builds a
one-shot synthetic worker that connects to a manually created
`caf_queue_test_p0_20261013_1` database in CAF PostgreSQL; `p0-code-test`
starts a separate PostgreSQL service on `127.0.0.1:55433` for a one-shot host
CLI worker. Neither is started by `services.sh up core`. The synthetic worker
refuses a connected database whose name does not start with `caf_queue_test_`.
The host code worker uses the existing user's CLI profiles and a worktree
outside the umbrella submodules; its CLI credentials are never mounted into
Docker. Its test PostgreSQL credentials are supplied from the local shell,
not from a repository file. `p0-test-daemon` starts a persistent polling
synthetic worker and the same isolated test PostgreSQL service. It has no CLI
authentication or connection to the core database. The profile dependency is
valid when enabled alone (`docker compose --profile p0-test-daemon config
--services` lists both services). Keep these profiles out of normal startup.
After exporting the run artifact, stop the test daemon and
`caf-p0-test-postgres-1`; its dedicated
`caf_p0_test_data` volume preserves the journal for review. See the
[measured experiment](../experiments/2026-10-13-p0-recovery-and-code.md).

## Credentials and first startup

Use an initialized recursive checkout. Supply credentials in your local shell environment; never put them in Git. `CAF_API_TOKEN` needs at least 32 characters. `CAF_POSTGRES_PASSWORD` needs at least 16 URL-safe characters from letters, digits, `.`, `_`, `~`, `-`; this restriction keeps the generated PostgreSQL URL unambiguous. **Keep the same PostgreSQL password across later `up core` calls for an existing data volume**: setting a new environment value does not change the password inside an initialized database. Store it in a user-controlled secret store outside the repository; do not paste real values into tickets or logs. The initial test session did not retain a reusable credential file. Example PowerShell setup for a new, empty volume:

```powershell
$env:CAF_API_TOKEN = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
$env:CAF_POSTGRES_PASSWORD = [Convert]::ToHexString([Security.Cryptography.RandomNumberGenerator]::GetBytes(24))
$env:CAF_API_PORT = '8123'
```

For **this existing local instance only**, a fresh PowerShell process can recover the original values from its still-existing CAF API container without printing them. This was exercised before a successful `down core`/`up core` cycle. Docker access already grants access to container environment variables. Use the values only in the current process and clear them afterward; this route stops working if the API container is removed. Keep a separate secure copy before that happens, or plan a controlled in-place PostgreSQL password rotation. Do not initialize a replacement database or delete the volume to address a lost password.

```powershell
$cafExisting = docker inspect --format '{{json .Config.Env}}' caf-control-api-1 | ConvertFrom-Json
$env:CAF_API_TOKEN = ($cafExisting | Where-Object { $_.StartsWith('CAF_API_TOKEN=') } | Select-Object -First 1).Substring(14)
$cafDbUrl = ($cafExisting | Where-Object { $_.StartsWith('CAF_DATABASE_URL=') } | Select-Object -First 1).Substring(17)
$env:CAF_POSTGRES_PASSWORD = ([uri]$cafDbUrl).UserInfo.Split(':')[1]
$env:CAF_API_PORT = '8123'
& 'C:\Program Files\Git\bin\bash.exe' scripts/services.sh up core
Remove-Item Env:CAF_API_TOKEN,Env:CAF_POSTGRES_PASSWORD,Env:CAF_API_PORT
$cafExisting = $null; $cafDbUrl = $null
```

Run the wrapper from the umbrella root in WSL or Git Bash after the API Dockerfile and image build have been checked. From Windows PowerShell on this host, call `C:\Program Files\Git\bin\bash.exe` explicitly; unqualified `bash` resolved to the WSL launcher and did not pass the temporary CAF environment to the wrapper during the 2026-10-13 attempt:

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

Development overrides/hot reload, resource tuning, abrupt failure recovery and additional safe cleanup procedures remain pending. See [verification](../development/verification.md) and [the P0 plan](../plans/2026-10-13-p0-vertical-slice.md).

## Startup blocker observed 2026-10-13

Before the attempt, host port 8123 had no listener, `caf` had no listed containers, and Docker Engine 29.8.2 responded while unrelated Compose projects were present. The first wrapper call through Windows' unqualified `bash` failed credential validation before Docker because it invoked WSL Bash without the temporary variables. A subsequent call through the explicit Git Bash executable passed that preflight but Docker returned `Docker Desktop is unable to start`. Follow-up read-only `docker version`, `docker ps` and CAF `ps` returned the same daemon error; `com.docker.service` showed `Stopped`. No Docker restart or operation on other projects was attempted. The temporary random CAF credentials were deleted. Service creation and database readiness could not be determined or tested after the daemon became unavailable.

## Live core check after Docker recovery

With separate authorization, Docker Desktop was restarted using `docker desktop restart`; Engine 29.8.2 responded afterward. The previously running containers seen in the available baseline returned to running/healthy status. No data or volumes were removed. The first successful CAF `up core` built the API image and produced healthy PostgreSQL and API containers, but `docker port caf-control-api-1` had no host binding and Windows `127.0.0.1:8123` refused connections. Its only network was `internal: true`. The API was then attached to a new non-internal `edge` network while PostgreSQL stayed on `private`; a second `up core` kept the same PostgreSQL container and volume and recreated only the API. Docker reported `127.0.0.1:8123->8000/tcp`; host `/health/live` and `/health/ready` each returned HTTP 200.

Against that live database, an unauthenticated `POST /v1/tasks` returned 401, an authenticated submission returned 201, a retry with the same idempotency key returned the same Run, and authenticated `GET /v1/runs/{id}` returned 200 with `queued` status. The same Run remained readable after restarting only the API container. A normal `down core` stopped both CAF containers without deleting `caf_postgres_data`; `up core` restored both to healthy and the same Run remained readable with HTTP 200. Before testing the normal group cycle, a fresh PowerShell process recovered the original credentials from the CAF API container environment; the environment values were cleared afterward. The one synthetic queued Run and its Task were then deleted by exact IDs and idempotency key so a future worker cannot claim the smoke request. `tasks` and `runs` each had zero rows afterward; readiness stayed at 200. This verifies normal group stop/start and P0 API persistence, not worker execution, abrupt database-failure recovery or the full SPEC core group.
