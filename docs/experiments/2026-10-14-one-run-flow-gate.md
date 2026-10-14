# One-Run Flow live gate

Date: 2026-10-14. Source: [SPEC sections 9-12 and 16](../../SPEC.md). This is
measured evidence from one explicitly approved Run, not P0 acceptance.

## Scope and result

- Published worker `1b14faa974fca168966c9c828c53b004c8489320` and umbrella
  `f6bbc69697501cde6f183b1e60d2a67084d627f3` in that order; both remote
  `main` refs were read back at the requested SHA.
- Used the clean sample base `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`,
  isolated database `caf_queue_test_flow_7ecb9d45`, loopback API and UI, and
  one exact-Run worker grant expiring in 45 minutes. The existing Codex and
  Claude CLI subscription login checks passed. No paid model API fallback was
  configured. No credentials or model transcript were saved as evidence.
- Run `f6be452b-b373-4e25-80e6-3ce27597e552`, attempt 1, completed
  `failed` after 13.1 seconds. The only recorded Flow stage was `plan`, with
  status `failed`, failure class `agent`, and workflow reason `plan_agent`.
  Iterations were zero. No implementation, acceptance test, review or real
  correction stage occurred. The recorded artifact did not distinguish a
  Claude CLI agent failure from an invalid structured plan response; no model
  output was retained, so the exact cause cannot be determined from this Run.
- PostgreSQL journal events were `claimed` and `completed`. The host UI read
  the same terminal Run status and returned `artifact=null` on its status
  response. The sample repository remained at its base revision, with no
  additional worktree or published sample code.

## Cleanup and next gate

The temporary API/UI/worker processes stopped, revoking the grant; ports
18124, 5175 and 55433 had no listener. The isolated database was dropped and
the CAF test PostgreSQL container stopped. The shared CAF database and
persistent worker were not used by this procedure. A safe machine-readable
summary is retained outside Git as `caf_flow_live_evidence.json` in the Codex
task directory.

The Flow fixture had a strict JSON plan parser that would reject a fenced
JSON object. An offline follow-up now accepts a single JSON fence while still
rejecting extra prose; this is a plausible compatibility fix, **not a proven
diagnosis** of the live failure. The one authorized Run is spent. A subsequent
real Flow Run, including implementation, tests, review and any correction,
requires a separate bounded approval and should record a safe, specific stage
failure reason without storing model text.
