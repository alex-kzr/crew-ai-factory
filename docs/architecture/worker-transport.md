# Host worker transport boundary

Source: [SPEC sections 5, 9–12 and 16](../../SPEC.md). Status: **implemented
in code and tested with dummy credentials; disabled in the live core**.

## Supported boundary

The control API remains bound to loopback. A prospective Windows host worker
would use `WorkerAPIStore` with an explicit `http://127.0.0.1:<port>` URL and a
separate `CAF_WORKER_TOKEN`. The client rejects any other host, scheme,
userinfo, path or redirect. It sends the token only in an Authorization header
and withholds URLs, response bodies and token material from transport errors.
Codex/Claude CLI authentication remains in the host user's existing context;
it is not copied or mounted into any container. The worker invokes the host
runtime in its own process, so there is no remote arbitrary-command endpoint.

The API's `/v1/worker/*` routes are **off** when `CAF_WORKER_TOKEN` is unset.
When configured, that token is distinct from `CAF_API_TOKEN`: the former
authorizes only queue database identity, one claim, lease/cancel inspection,
renewal, guarded completion, expired-lease quarantine and Run readback. The
latter continues to authorize task intake and ordinary Run status/cancel.
Input owners follow the storage owner format, leases are limited to 15–3600
seconds, and completion artifacts are capped at 128 KiB. PostgreSQL remains
the authority for owner, live lease, cancel request, attempt and the
transactional claim/completion/quarantine journal. No HTTP response grants a
command, filesystem path or CLI permission.

The current real-code host fixture additionally requires a connected
`caf_queue_test_*` database, exact sample repository, base revision and task
prompt, clean checkout, external worktree and an existing native Codex
executable. It allows only the fixture implementation file and performs one
Codex call, deterministic gates and a no-tools Claude review. These checks
bound the **test fixture**; a worktree is not a security sandbox and this does
not make arbitrary user code safe for automatic dispatch.

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

## Evidence and grant boundary

API route tests with dummy tokens verified disabled-by-default behavior,
token separation, owner guards and artifact bounds. An opt-in in-process API
test used a separate `caf_queue_test_*` database and dummy worker token to
exercise claim, renewal, completion and journal readback. Worker client tests
verified loopback restriction, redirect refusal, response validation and
credential-free errors. No actual worker token has been created or placed in
a container or host daemon. Enabling the long-lived host transport would add
a new persistent credential grant and therefore requires an explicit decision.
Do not set `CAF_WORKER_TOKEN` in core or start a host API worker until then.
