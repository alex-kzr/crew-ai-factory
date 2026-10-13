"""Synthetic CAF workflow against the pinned sample fixture; no coding CLI is invoked."""

from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_REPO = ROOT / "repositories" / "caf-agent-runtime"
WORKER_REPO = ROOT / "repositories" / "caf-orchestration-worker"
SAMPLE_REPO = ROOT / "repositories" / "caf-sample-app"
sys.path[:0] = [str(RUNTIME_REPO / "src"), str(WORKER_REPO / "src")]

from caf_agent_runtime import AgentEvent, AgentResult, AgentStatus, CodingTask  # noqa: E402
from caf_orchestration_worker import RunRequest, run_baseline, write_artifact  # noqa: E402


def git(*args: str, cwd: Path = SAMPLE_REPO) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return result.stdout.strip()


class FixtureRuntime:
    """Benchmark-specific deterministic double; it is not a CLI or production adapter."""

    def __init__(self) -> None:
        self.statuses: dict[str, AgentStatus] = {}

    async def execute(self, task: CodingTask, workspace: Path, session_id: str | None = None) -> AgentResult:
        source = workspace / "src" / "caf_sample" / "orders.py"
        output: dict[str, object] = {}
        changed_files: tuple[str, ...] = ()
        exit_code: int | None = None
        if task.operation == "plan":
            output = {"tasks": ["discount-code"]}
        elif task.operation == "implement":
            output = {"note": "deliberately incomplete first pass"}
        elif task.operation == "review":
            approved = "discount_code: str | None = None" in source.read_text(encoding="utf-8")
            output = {"approved": approved, "findings": [] if approved else ["discount_code is absent"]}
        elif task.operation == "correct":
            body = source.read_text(encoding="utf-8")
            changes = (
                ("def quote_order(items: list[LineItem]) -> Quote:",
                 "def quote_order(items: list[LineItem], discount_code: str | None = None) -> Quote:"),
                ("    shipping_cents = (\n",
                 "    discount_cents = 0\n"
                 "    if discount_code is not None:\n"
                 "        if discount_code.strip().upper() != \"SAVE10\":\n"
                 "            raise ValueError(\"unknown discount code\")\n"
                 "        discount_cents = (subtotal_cents * 10 + 50) // 100\n\n"
                 "    shipping_cents = (\n"),
                ("        discount_cents=0,", "        discount_cents=discount_cents,"),
                ("        total_cents=subtotal_cents + shipping_cents,",
                 "        total_cents=subtotal_cents - discount_cents + shipping_cents,"),
            )
            for before, after in changes:
                if body.count(before) != 1:
                    raise AssertionError(f"fixture patch anchor changed: {before!r}")
                body = body.replace(before, after, 1)
            source.write_text(body, encoding="utf-8")
            changed_files = ("src/caf_sample/orders.py",)
            output = {"note": "deterministic fixture correction"}
        elif task.operation == "test":
            env = os.environ.copy()
            env["PYTHONPATH"] = str(workspace / "src")
            completed = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                cwd=workspace, env=env, capture_output=True, text=True, timeout=30, check=False,
            )
            exit_code = completed.returncode
            output = {"passed": exit_code == 0, "suite": "sample-app unittest acceptance"}
        else:
            raise ValueError(f"unexpected operation: {task.operation}")
        self.statuses[task.run_id] = AgentStatus.SUCCEEDED
        return AgentResult(
            run_id=task.run_id, correlation_id=task.correlation_id, status=AgentStatus.SUCCEEDED,
            summary=f"synthetic {task.operation}",
            events=(AgentEvent(task.run_id, task.correlation_id, 1, "completed", task.operation),),
            changed_files=changed_files, exit_code=exit_code, output=output,
        )

    async def cancel(self, run_id: str) -> None:
        self.statuses[run_id] = AgentStatus.CANCELLED

    async def get_status(self, run_id: str) -> AgentStatus:
        return self.statuses[run_id]


class SyntheticFixtureIntegrationTest(unittest.TestCase):
    def test_review_correction_and_real_acceptance_gate_in_external_worktree(self) -> None:
        base_revision = git("rev-parse", "discount-code-base-v1")
        with tempfile.TemporaryDirectory(prefix="caf-synthetic-") as temporary:
            worktree = Path(temporary) / "worktree"
            git("worktree", "add", "--detach", str(worktree), base_revision)
            original = (worktree / "src" / "caf_sample" / "orders.py").read_bytes()
            try:
                request = RunRequest(
                    "fixture-run", "fixture-correlation", "Add discount_code", "synthetic",
                    max_corrections=1, base_revision=base_revision,
                )
                artifact = asyncio.run(run_baseline(request, FixtureRuntime(), worktree))
                report_path = Path(temporary) / "artifact.json"
                write_artifact(artifact, report_path)
                report = json.loads(report_path.read_text(encoding="utf-8"))
                self.assertEqual(report["status"], "succeeded")
                self.assertEqual(report["base_revision"], base_revision)
                self.assertEqual(report["iterations"], 1)
                self.assertEqual(
                    [stage["operation"] for stage in report["stages"]],
                    ["plan", "implement", "review", "correct", "review", "test"],
                )
                self.assertFalse(report["stages"][2]["output"]["approved"])
                self.assertEqual(report["stages"][-1]["output"]["passed"], True)
                self.assertEqual(report["stages"][-1]["exit_code"], 0)
                self.assertEqual(report["stages"][3]["changed_files"], ["src/caf_sample/orders.py"])
                self.assertTrue(all(stage["events"][0]["correlation_id"] == "fixture-correlation" for stage in report["stages"]))
                self.assertEqual(git("diff", "--name-only", cwd=worktree), "src/caf_sample/orders.py")
            finally:
                (worktree / "src" / "caf_sample" / "orders.py").write_bytes(original)
                git("worktree", "remove", str(worktree))


if __name__ == "__main__":
    unittest.main()
