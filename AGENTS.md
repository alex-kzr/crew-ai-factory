# CAF agent instructions

This is an independent project. Read `SPEC.md` and `docs/README.md` before implementation. Treat SPEC as the authority; mark assumptions and measured facts separately. Keep documentation in English and update it with code. Do not import architecture or code from other factory projects by analogy.

Do not commit secrets, CLI auth, runtime worktrees, logs, build outputs or `.env`. Do not run CLIs through interpolated shell commands. Do not claim a service, Compose group, CrewAI feature, or CLI behavior is verified until tested. Worktrees belong outside submodule directories. Never push, open PRs, or merge generated code automatically without an explicit approval policy.
