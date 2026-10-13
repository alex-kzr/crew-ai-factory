# Child repositories and publication

Source: [SPEC §4](../../SPEC.md). The umbrella pins Git commit IDs for these five independent repositories. Logical service names in the architecture remain unchanged; only repository directory names now match the GitHub repositories.

| Directory | Configured `origin` | Role |
|---|---|---|
| `repositories/caf-control-api` | `https://github.com/alex-kzr/caf-control-api` | API |
| `repositories/caf-orchestration-worker` | `https://github.com/alex-kzr/caf-orchestration-worker` | CrewAI orchestration |
| `repositories/caf-agent-runtime` | `https://github.com/alex-kzr/caf-agent-runtime` | CLI execution boundary |
| `repositories/caf-web-ui` | `https://github.com/alex-kzr/caf-web-ui` | UI |
| `repositories/caf-sample-app` | `https://github.com/alex-kzr/caf-sample-app` | Reproducible coding target |

The umbrella `origin` remains `https://github.com/alex-kzr/crew-ai-factory`. On 2026-10-13, the five initial `main` commits and umbrella commit `0fbd69f` were pushed. Read-only remote SHA checks matched all six local commits, and a fresh `git clone --recurse-submodules` checked out all five pinned gitlinks.

## Publication sequence

1. Confirm each child remote is still empty or that its history is compatible with the pinned local commit. Never force-push or overwrite an unrelated initial commit.
2. Push each child's local `main` branch to its configured `origin`, establishing upstream tracking. Verify the remote advertises the exact pinned commit.
3. Commit/push the umbrella change after all child commits are reachable. From a disposable fresh clone, run `git submodule update --init --recursive` and compare the five checked-out commits with the umbrella gitlinks.
4. Implement `scripts/bootstrap.sh` to initialize submodules and check tools without printing secrets; test in a fresh checkout. The script is not yet present.

To update a child later, commit and push within that child, then stage and commit the changed gitlink in the umbrella. To add another child, justify its separate lifecycle in an ADR, publish it, add it as a submodule, and test fresh bootstrap. Runtime task worktrees must never be created inside these directories.
