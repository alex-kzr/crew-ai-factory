# Bounded P0 CLI, inspection and crash gate

Date: 2026-10-14. Source: [SPEC sections 5, 9-12, 14 and 16](../../SPEC.md).
This records measured facts from an approved isolated run, separate from the
remaining P0 acceptance requirements. The safe machine-readable summary is
saved outside Git as `caf_p0_live_evidence.json` in this Codex task directory.

## Boundary and inputs

- Reused the existing Codex and Claude CLI subscriptions. Both filtered-env
  `login status` calls and both version calls exited 0; auth output was not
  printed or retained. No paid API fallback was configured.
- Used sample base `e12f4d8293ea0dd8a5e18c3006af803c4d429b56`, one
  disposable host worktree per Run outside submodules, a private
  `caf_queue_test_live_20261014_13177a` PostgreSQL database on the existing
  opt-in test container, and a temporary API on `127.0.0.1:18123`.
- Used two distinct exact-Run worker grants, each with an expiry of 30 or 15
  minutes. Tokens were generated in supervisor memory, passed by child
  environment, never printed or saved, and revoked by stopping/restarting
  the temporary API without grant fields. The first grant was revoked by
  stopping its API; the second old token subsequently received HTTP 503.
  The shared `caf` database had zero Runs before and after.
- Actual count: one normal Run, one controlled crash Run, no additional
  normal Run. The normal worker measured 80.5 seconds; the crash gate ran
  about 35 seconds. Both are below the 30-minute per-Run and 90-minute total
  limits. The normal fixture allowed zero corrections, as its current worker
  implementation requires.

## Normal Run and inspection

Run `03d0ea10-16ac-4769-8a07-32e72ea7ea8b` completed `succeeded`, attempt
1. Codex produced a local, unpushed sample commit
`d54c85193dde49bbd3ae2fe4d82c55015074c715`. Both baseline and
discount-code acceptance suites passed; Claude's structured verdict was
`approved=true` with zero findings. The SQL-backed `/results` and `/events`
routes returned a matching terminal status and ordered `claimed, completed`
lease events.

The first host UI startup failed because its CLI entrypoint referenced an
undefined `uiPort`. That code path was fixed and given a CLI startup test.
After the fix, a new temporary API **without a worker grant** and the host UI
served the existing Run. The built HTML, config, Run, results and events
routes returned HTTP 200; the Run status and result status matched, and the
UI's status response had `artifact=null`. This verifies the same-origin HTTP
read path and existing React/mock rendering contract, not remote user
identity authentication or a browser visual acceptance test.

## Controlled real-CLI crash

Run `b47b8dc5-7bed-44d5-a52d-0ef473584e4b` used a 30-second lease. The
host worker claimed it and launched a real Codex native process under the
Windows Job Object path. The test observed that child PID in the worker's
process tree, terminated only the test worker, and verified that the child
disappeared without manual cleanup. After the real database lease expired,
scoped quarantine recorded `failed/orphan_unverified`, attempt 1 and
`claimed, quarantined` events. Another claim returned no Run. A second
quarantine was unnecessary; this test establishes no replay for this Run,
not general recovery of all possible provider processes.

The private crash worktree was removed only after child exit was verified.
Temporary host APIs and UI were stopped, the test PostgreSQL container was
stopped while retaining its dedicated volume, and ports 18123 and 5174 had
no listeners. No generated sample code was pushed or merged.

## Remaining gates

This path uses a fixture-specific one-shot worker, not the complete SPEC
`core` group. It does not run the complete CrewAI Flow in one Run, exercise a
negative review followed by bounded correction, prove all process descendants
on all hosts, provide multi-user browser authorization, or produce a Mode
A/B/C benchmark verdict. The successful code Run and crash Run are separate.
