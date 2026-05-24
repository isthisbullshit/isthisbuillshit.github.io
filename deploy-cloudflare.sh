#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v wrangler >/dev/null 2>&1; then
  echo "wrangler is required but was not found in PATH" >&2
  exit 1
fi

echo "Deploying backend worker..."
(
  cd "$SCRIPT_DIR/backend"
  wrangler deploy
)

echo "Deploying root worker..."
(
  cd "$SCRIPT_DIR"
  wrangler deploy
)

echo "Cloudflare deploy complete."
