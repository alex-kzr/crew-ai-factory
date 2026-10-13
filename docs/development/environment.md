# Local environment facts (2026-10-13)

Read-only version checks in the CAF checkout returned: Python 3.12.9, uv 0.12.17, Git 2.46.1.windows.1, Docker 29.8.2, Docker Compose 5.5.1, Codex CLI 0.162.1, and Claude Code 2.1.296. CrewAI was not installed in the default Python environment. `codex login status` and `claude auth status` each exited 0; no credential data was printed or copied.

These facts do not verify non-interactive CLI flags, model/API costs, Docker runtime authentication, subprocess cancellation, or CrewAI capabilities. The first milestone uses only a synthetic adapter. Real CLI tests must use the existing profiles and a disposable target repository after the synthetic contract passes.
