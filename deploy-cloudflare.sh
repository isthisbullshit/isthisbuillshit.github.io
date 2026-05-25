#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v npx >/dev/null 2>&1; then
  echo "npx is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is required but was not found in PATH" >&2
  exit 1
fi

if ! command -v grep >/dev/null 2>&1; then
  echo "grep is required but was not found in PATH" >&2
  exit 1
fi

echo "Deploying backend worker..."
(
  cd "$SCRIPT_DIR/backend"
  uvx --from workers-py pywrangler deploy
)

echo "Deploying root worker..."
(
  cd "$SCRIPT_DIR"
  npx wrangler deploy
)

echo "Cloudflare deploy complete."
