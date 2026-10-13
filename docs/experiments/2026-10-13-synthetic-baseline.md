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

## Mode status and limits at this initial check

- Mode C: a sequential `asyncio` baseline with synthetic runtime is runnable. It does not perform real agent execution or Git integration by itself.
- Mode B: CrewAI Flow was pending at this initial check; CrewAI was not installed in the checked Python environments. A later [Flow and CLI experiment](2026-10-13-flow-cli-and-api.md) implemented and tested synthetic Mode B. No API/model configuration was selected for this initial check.
- Mode A: Crew-as-Tool pending; manager LLM and cost requirements must be verified before a comparable run.

No timing, code-quality or cost comparison across Modes A/B/C was possible from these initial checks. The [follow-up experiment](2026-10-13-flow-cli-and-api.md) records later CLI path checks and synthetic Flow parity; it does not establish a benchmark verdict.
