# Host worker transport boundary

Source: [SPEC sections 5, 9-12 and 16](../../SPEC.md). Status: **scoped
contract implemented and tested with dummy tokens; disabled in live core**.

## Supported boundary

The host client uses an explicit `http://127.0.0.1:<port>` URL and a separate
`CAF_WORKER_TOKEN`. It rejects other hosts, schemes, userinfo, paths, redirects
and environment proxies. It sends the token only in an Authorization header
and withholds URLs, response bodies and token material from transport errors.
Codex/Claude CLI authentication remains in the host user's existing context;
it is not copied or mounted into any container. The worker invokes the host
runtime in its own process, so there is no remote arbitrary-command endpoint.

The API's `/v1/worker/*` routes are **off** unless the complete grant is
configured. It binds one token to one identity, exact `caf_queue_test_*`
database, Run and Task IDs, repository, workspace ID, base revision, provider
and timezone-aware expiry at most one hour ahead. Missing or unknown scope
fails closed. The connected database identity and expiry are checked on each
request. Claim and expired-lease quarantine filter on all Run/Task scope
fields **inside their SQL mutations**, before any unrelated Run can be
claimed or changed. Readback checks the same scope; lease/control/completion
also require the exact Run and the configured owner. The bearer cannot choose
a different trusted owner. `CAF_API_TOKEN` remains separate for task intake.
Leases are limited to 15-3600 seconds, and completion artifacts to 128 KiB.
PostgreSQL remains the authority for owner, live lease, cancel request,
attempt and transactional claim/completion/quarantine journal. No HTTP
response grants a command or CLI permission.

`workspace_id` is an explicit Task label checked before claim. The one-shot
host entrypoints now map exact IDs to the checked `caf-sample-app` submodule
under `CAF_UMBRELLA_ROOT`, rejecting unknown IDs and redirected checkouts.
The real-code fixture accepts only `caf-sample-fixture-v1` for HTTP, a fixed
sample base and source file. It creates a private worktree directory under a
checked host temporary root for each invocation. The synthetic HTTP entrypoint
accepts only `caf-synthetic-v1`. There is no wildcard grant or grant for the
shared `caf` database. The one-Run grant cannot read a different source Run;
the HTTP fixture explicitly blocks `CAF_REVIEW_SOURCE_RUN` continuation.

The current real-code host fixture additionally requires a connected
`caf_queue_test_*` database, exact sample repository, base revision and task
prompt, clean checkout, external worktree and an existing native Codex
executable. It allows only the fixture implementation file and performs one
Codex call, deterministic gates and a no-tools Claude review. These checks
bound the **test fixture**; a worktree is not a security sandbox and this does
not make arbitrary user code safe for automatic dispatch. CLI, Git and test
children now receive an explicit minimal environment with OS lookup and user
profile/provider config paths. Worker/database tokens and model API keys are
excluded. Provider login has not been retested since this environment change.

## Failure behavior

- A 401/503, timeout, malformed response or redirect fails the client without
  exposing the bearer token. When transport fails during active execution,
  the dispatcher stops its executor and leaves the claim unacknowledged.
- A lost lease or cancellation stops the executor before terminal ACK.
  Conditional completion requires the current owner and unexpired lease.
- Expired running work enters `failed/orphan_unverified`; there is no automatic
  model replay. Unverified process-tree cleanup propagates and preserves the
  worktree for investigation.
- A partial Git worktree-add failure may leave a private directory for manual
  inspection; cleanup does not recursively delete an unverified worktree.
- The API routes do not start CLIs; the live core has no worker token and no
  always-on real-CLI worker.
- Expiry rejects new requests. Revocation means removing or replacing the
  grant and restarting the API; no refresh or multi-token grace period exists.
  An in-flight Run may then lose its lease and require scoped quarantine.

## Evidence and grant boundary

API route tests with dummy tokens verified disabled-by-default behavior,
token separation, expiry, owner, database, workspace and Run scope and
artifact bounds. An opt-in in-process API test used separate
`caf_queue_test_*` PostgreSQL and dummy worker token to exercise an unrelated
Run refusal, wrong workspace refusal, exact claim, renewal, completion and
journal readback. Worker tests verified loopback/proxy/redirect handling and
credential-free errors. A native child-process test verified that dummy
worker/model tokens did not reach a launched process. With explicit approval,
a [temporary synthetic HTTP check]
(../experiments/2026-10-13-scoped-http-procedure.md#measured-result-2026-10-13)
then passed over a real loopback socket for one isolated Run, including
foreign-Run denial and revocation. Its ephemeral token and processes were
removed. Core Compose does not pass `CAF_WORKER_TOKEN` through and no live
core grant, real provider login retest or long-lived real CLI worker is
claimed. An [offline host crash check]
(../experiments/2026-10-13-offline-workspace-and-recovery.md) passed with a
disposable Python child and fake in-memory queue state; it does not prove
PostgreSQL crash recovery or real CLI containment. A later, separately
approved [PostgreSQL and HTTP crash/restart check]
(../experiments/2026-10-13-postgres-http-crash-restart.md) verified real lease
expiry, durable quarantine and no replay after API restart for one disposable
Python child. Real CLI containment and provider login with the filtered child
environment remain unverified. These checks do not enable real CLI dispatch.
