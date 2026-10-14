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

## Retrospective diagnostic gap

The original `plan_agent` value merges two paths in the code that ran: Claude
CLI could exit nonzero with an unrecognized agent error, or it could exit 0
and return text rejected by the plan parser. The reported 13.1-second elapsed
time and `agent` failure class do not distinguish those paths. Timeout has a
separate failure class in the adapter. The stored artifact omitted CLI exit
code, captured response size, parse outcome and a safe stage category. The
isolated database was dropped during the approved cleanup, and neither model
text nor a detailed CLI result was retained. The exact cause is therefore
**not recoverable from available evidence**.

An offline-only change now records a fixed-shape diagnostic for Flow plan and
review: stage phase, correlation ID, category, provider status/failure class,
exit code, size of the redacted and capped response capture, input format and
parser outcome. No stdout, stderr, raw prompt or transcript enters this
diagnostic. Complete plain JSON and one complete JSON code fence are supported;
extra prose and invalid schema remain rejected. Synthetic fixtures cover
those formats and failure classes, but do not prove how Claude responded in
the previous Run.

The smallest next live experiment, if separately approved, is one isolated
no-tools plan attempt with this diagnostic enabled. An offline follow-up added
`p0_plan_worker`, a separate one-Run entrypoint that accepts only a Claude
claim with zero corrections and terminates after the plan. It does not
construct the Codex runtime. Tests cover valid and invalid plans and show no
writer, review or correction call. The plan-only path is **not live verified**.
Inspect the terminal Run's category and parser outcome before deciding whether
any broader coding Run is warranted. Keep the test database and its audit
records, stop the container and revoke the exact-Run grant; do not drop the
database as part of automatic cleanup. No new model call or grant was made for
this offline follow-up.

A separate read-only review of this change found no critical diagnostic
leakage. It noted that `auth_limit` is an error signal rather than a proven
provider cause, and that structured review findings remain part of the
ordinary Run artifact outside this fixed-shape diagnostic. Those findings
must not be copied into the safe experiment summary.

The later [plan-only schema gate](2026-10-14-plan-only-schema-gate.md) records
the separately approved plan-only Run and its subsequent offline contract fix.
