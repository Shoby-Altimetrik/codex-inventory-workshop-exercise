#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Starting backend on http://localhost:8001 ..."
(
  cd "$ROOT_DIR/server"
  if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
    "$ROOT_DIR/.venv/bin/python" main.py
  elif command -v uv >/dev/null 2>&1; then
    uv run python main.py
  else
    echo "Warning: .venv not found. Falling back to system python3." >&2
    echo "Recommended setup: python3 -m venv .venv && source .venv/bin/activate && pip install -r server/requirements.txt pytest httpx" >&2
    python3 main.py
  fi
) &
BACKEND_PID=$!

echo "Starting frontend on http://localhost:3000 ..."
(
  cd "$ROOT_DIR/client"
  if [[ ! -d node_modules ]]; then
    echo "Installing frontend dependencies..."
    npm install
  fi
  npm run dev
) &
FRONTEND_PID=$!

cleanup() {
  echo "Stopping services..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM
wait
