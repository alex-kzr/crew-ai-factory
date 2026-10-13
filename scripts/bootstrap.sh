#!/usr/bin/env bash
set -euo pipefail

if ! command -v git >/dev/null 2>&1; then
  printf 'Git is required to bootstrap CAF.\n' >&2
  exit 1
fi

repo_root="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
git -C "$repo_root" submodule sync --recursive
git -C "$repo_root" submodule update --init --recursive
printf 'CAF submodules are checked out at the umbrella gitlinks.\n'
git -C "$repo_root" submodule status
