#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
compose_file="$project_root/infrastructure/compose/compose.yaml"

usage() {
  cat <<'EOF'
Usage: scripts/services.sh <command> [group-or-service]

Commands:
  up core          Build and start the current API + PostgreSQL slice.
  down core        Stop only the current core services; retain the database volume.
  status | ps      Show containers in the caf project.
  logs core        Show logs for the current core services.
  logs SERVICE     Show logs for control-api or postgres.
  config           Validate/show the Compose model without interpolating secrets.
  build core       Build the control-api image.

The worker, runtime, Redis, UI and observability groups are not yet runnable.
EOF
}

fail() { printf 'CAF: %s\n' "$*" >&2; exit 2; }

compose() {
  docker compose --project-name caf --file "$compose_file" "$@"
}

require_core_credentials() {
  [[ ${CAF_API_TOKEN:-} =~ ^.{32,}$ ]] || fail 'CAF_API_TOKEN must contain at least 32 characters.'
  [[ ${CAF_POSTGRES_PASSWORD:-} =~ ^[A-Za-z0-9._~-]{16,}$ ]] || fail 'CAF_POSTGRES_PASSWORD must contain at least 16 URL-safe characters (letters, digits, . _ ~ -).'
}

require_current_core() {
  case "${1:-}" in
    core) ;;
    ui|observability|dev|all) fail "group '$1' is not runnable yet; only the current API + PostgreSQL core slice exists." ;;
    *) fail "expected group 'core'; received '${1:-<none>}'" ;;
  esac
}

command_name="${1:-}"
target="${2:-}"
if [[ $# -gt 2 ]]; then fail 'too many arguments'; fi

case "$command_name" in
  up)
    require_current_core "$target"
    require_core_credentials
    compose --profile core up --detach --build --wait control-api postgres
    ;;
  down)
    require_current_core "$target"
    # Only today's two core services exist. Revisit ownership before adding
    # a group that can share postgres with another active service.
    compose --profile core stop control-api postgres
    ;;
  status|ps)
    [[ -z $target ]] || fail "'$command_name' takes no target"
    compose --profile core ps --all
    ;;
  logs)
    case "$target" in
      core) compose --profile core logs --tail=100 --no-color control-api postgres ;;
      control-api|postgres) compose --profile core logs --tail=100 --no-color "$target" ;;
      ui|observability|dev|all) fail "group '$target' is not runnable yet" ;;
      *) fail "expected 'core', 'control-api' or 'postgres'" ;;
    esac
    ;;
  config)
    [[ -z $target ]] || fail "'$command_name' takes no target"
    compose --profile core config --no-interpolate
    ;;
  build)
    require_current_core "$target"
    compose --profile core build control-api
    ;;
  help|-h|--help|'')
    usage
    ;;
  *) fail "unknown command '$command_name'" ;;
esac
