# Child repositories and publication

Source: [SPEC §4](../../SPEC.md). The umbrella pins Git commit IDs for these five independent repositories:

| Directory | Suggested future GitHub repository name | Role |
|---|---|---|
| `repositories/control-api` | `crew-ai-factory-control-api` | API |
| `repositories/orchestration-worker` | `crew-ai-factory-orchestration-worker` | CrewAI orchestration |
| `repositories/agent-runtime` | `crew-ai-factory-agent-runtime` | CLI execution boundary |
| `repositories/web-ui` | `crew-ai-factory-web-ui` | UI |
| `repositories/sample-app` | `crew-ai-factory-sample-app` | reproducible coding target |

These names are **recommendations, not existing GitHub repositories or URLs**. Child remotes were not created or pushed. The umbrella `origin` points to the explicitly supplied `https://github.com/alex-kzr/crew-ai-factory`; that URL has not been verified or pushed by this scaffold.

## Current local limitation

`.gitmodules` records absolute paths to local seed repositories because no child remotes exist. The checked-out submodules are usable on this machine, but a fresh checkout elsewhere cannot initialize them. Git stores each child as a gitlink in the umbrella, not copied source. Do not publish the umbrella until each seed commit is reachable from its child remote and `.gitmodules` contains those actual remote URLs.

## Publication sequence (after the user creates child remotes)

1. Obtain exact remote URLs for the five newly created repositories. In each checked-out child, inspect `git remote -v`; its cloned `origin` currently points to the local seed. After the exact new URL is supplied, replace that `origin` with `git remote set-url origin <actual-url>` and push its initial `main` commit. Do not create guessed remotes.
2. In the umbrella, run `git submodule set-url repositories/<name> <actual-url>` for each child, then `git submodule sync --recursive`. Commit `.gitmodules` and any updated gitlinks.
3. From a disposable fresh clone, run `git submodule update --init --recursive`; verify every pinned commit is reachable. Only then publish/update the umbrella remote.
4. Implement `scripts/bootstrap.sh` to initialize submodules and check tools without printing secrets; test in a fresh checkout.

To update a child later, commit and push within that child, then stage and commit the changed gitlink in the umbrella. To add a new child, justify its separate lifecycle/ownership in an ADR, create and publish it, add as a submodule, and test fresh bootstrap. Runtime task worktrees must never be created inside these directories.
