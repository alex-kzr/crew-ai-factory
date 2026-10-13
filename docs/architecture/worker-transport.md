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

`workspace_id` is an explicit Task label checked before claim. It does not
prove which host directory a worker opened: the worker must map that label to
an allowed path and verify its checkout. The real-code fixture accepts only
`caf-sample-fixture-v1` for HTTP, a fixed sample base and source file. The
one-shot synthetic HTTP entrypoint accepts only `caf-synthetic-v1`. There is
no wildcard grant or grant for the shared `caf` database.

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
worker/model tokens did not reach a launched process. No live HTTP socket
test, real provider login retest, or long-lived real CLI worker is claimed.
No actual worker token has been created or installed. Core Compose no longer
passes `CAF_WORKER_TOKEN` through. A [temporary synthetic HTTP procedure]
(../experiments/2026-10-13-scoped-http-procedure.md) defines the next consent
gate; it does not enable real CLI dispatch.
