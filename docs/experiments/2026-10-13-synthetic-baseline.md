# Synthetic baseline experiment — 2026-10-13

Source: [SPEC §§7, 10, 14–16](../../SPEC.md). This is an initial **synthetic contract test**, not the CrewAI comparison verdict or a completed P0 proof of concept.

## Reproducible inputs

- Sample target: `caf-sample-app`, tag `discount-code-base-v1` at commit `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`.
- Task: [add `discount_code`](../../repositories/caf-sample-app/tasks/discount-code.md).
- Runner: `python -m unittest discover -s tests/integration -p test_synthetic_fixture.py -v` from umbrella root.
- Runtime: benchmark-specific in-process deterministic double implementing the provider-neutral protocol. It does not invoke Codex or Claude and does not model their quality, cost or timing.

## Observed checks

| Check | Result |
|---|---|
| Runtime package tests | 21 passed on Python 3.12.9 |
| Worker package tests | 13 passed on Python 3.12.9 |
| Sample baseline | 5 passed |
| Sample acceptance at base commit | Fails as designed because `discount_code` is absent |
| Umbrella integration test | 1 passed; creates and cleans an external Git worktree |

The integration test observed the stage order `plan → implement → review(rejected) → correct → review(approved) → test(passed)`, one correction iteration, a matching base revision and correlation ID, a changed `orders.py`, and a passing real unittest acceptance gate after a deterministic fixture patch. It wrote and read a JSON artifact in a temporary directory. The worker's standalone `synthetic-demo` writes an artifact to an explicitly supplied path. No commit was created for the synthetic code change.

## Mode status and limits

- Mode C: a sequential `asyncio` baseline with synthetic runtime is runnable. It does not perform real agent execution or Git integration by itself.
- Mode B: CrewAI Flow pending; CrewAI was not installed in checked Python environments. No API/model configuration was selected.
- Mode A: Crew-as-Tool pending; manager LLM and cost requirements must be verified before a comparable run.

No timing, code-quality or cost comparison across Modes A/B/C is possible from these checks. Next: verify real CLI command paths using existing profiles and a disposable worktree, then integrate the same fixture and gates into Flow and baseline modes before making a verdict.
