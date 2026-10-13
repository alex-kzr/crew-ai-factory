# Synthetic fixture integration test

Run from the umbrella repository root with Python 3.12+ and Git:

```sh
python -m unittest discover -s tests/integration -p test_synthetic_fixture.py -v
```

The test creates a detached worktree from `caf-sample-app` tag `discount-code-base-v1` under the system temporary directory, outside every tracked submodule. A benchmark-specific deterministic test double simulates an incomplete implementation, a negative review, a correction, a second review and an actual standard-library acceptance-test run. It writes a JSON run artifact to that temporary directory, verifies the result and removes the worktree. No coding CLI, CrewAI, Docker or network call occurs. This tests the contract and gate sequence; it is not evidence of autonomous coding.

The fixture patch is deliberately contained in this test. Production runtime adapters must not embed benchmark-specific code changes. See [synthetic experiment report](../../docs/experiments/2026-10-13-synthetic-baseline.md).
