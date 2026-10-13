# Local environment facts (2026-10-13)

Read-only version checks in the CAF checkout returned: Python 3.12.9, uv 0.12.17, Git 2.46.1.windows.1, Docker 29.8.2, Docker Compose 5.5.1, Codex CLI 0.162.1, and Claude Code 2.1.296. CrewAI was not installed in the default Python environment. `codex login status` and `claude auth status` each exited 0; no credential data was printed or copied.

Subsequent checks verified installed non-interactive flags and a no-tools Claude Code call through the host adapter using the existing profile. A read-only Codex call failed with an authentication-category diagnostic despite the login status check. No CLI code-change task, Docker authentication path or complete process-tree cleanup has been verified. CrewAI 1.15.27 Flow listeners ran the synthetic baseline stages without constructing an Agent or LLM; this does not establish Mode A behavior or model/API costs. See the [follow-up evidence](../experiments/2026-10-13-flow-cli-and-api.md).
