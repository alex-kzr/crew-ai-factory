# Consolidated request for remaining live P0 gates

Source: [SPEC sections 9-12, 14 and 16](../../SPEC.md). The actions below are
**planned, not authorized or executed by this document**. Reuse the current
architecture and existing provider profiles; create no credentials or durable
permission grants. Request one explicit approval for this bounded sequence:

1. Run read-only `codex login status` and `claude auth status` under the
   filtered child environment, recording versions and pass/fail only.
2. On a private isolated `caf_queue_test_*` database and loopback API, issue
   a separate temporary, exact-Run host grant for each approved Run, with
   at most three grants in total. Execute at most two real provider
   Runs against `caf-sample-app` at pinned base revisions, in worktrees
   outside submodules. Bound each Run to one task, at most three corrections,
   30 minutes, and the current review/test gates. Preserve diffs and result
   metadata without credentials or model transcripts in the repository.
3. Use at most one additional controlled failure Run for real CLI process
   termination, lease expiry, quarantine and no automatic replay. Revoke
   temporary grants, stop isolated services, and remove disposable worktrees
   after evidence capture. Do not push, merge, deploy or touch shared data.
4. Check the new results/events routes against that isolated PostgreSQL/API
   instance and read the one approved Run via the host UI. Confirm the raw
   artifact is absent from the browser status response and handle snapshot
   races explicitly.

The operator must identify suitable pinned sample revisions, approve the
specific model calls and any service/test Run creation, and set a cost/time
ceiling before execution. A human identity mechanism for a remote or
multi-user browser UI is a separate design gate. Passing this sequence would
still require review against every remaining SPEC P0 acceptance criterion.
