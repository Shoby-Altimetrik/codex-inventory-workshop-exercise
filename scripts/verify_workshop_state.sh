#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: ./scripts/verify_workshop_state.sh --mode baseline|solved

Modes:
  baseline  Confirm expected intentional failures and no infra/import blockers.
  solved    Confirm all workshop backend/frontend tests pass.
EOF
}

MODE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

if [[ "$MODE" != "baseline" && "$MODE" != "solved" ]]; then
  usage
  exit 1
fi

cd "$ROOT_DIR"

if [[ ! -d ".venv" ]]; then
  echo "Error: .venv not found."
  echo "Setup:"
  echo "  python3 -m venv .venv"
  echo "  source .venv/bin/activate"
  echo "  pip install -r server/requirements.txt pytest httpx"
  exit 1
fi

read -r PYTHON_MAJOR PYTHON_MINOR < <("./.venv/bin/python" -c 'import sys; print(sys.version_info.major, sys.version_info.minor)')
if (( PYTHON_MAJOR < 3 || (PYTHON_MAJOR == 3 && PYTHON_MINOR < 11) )); then
  echo "Error: .venv is using Python ${PYTHON_MAJOR}.${PYTHON_MINOR}, but the workshop requires Python 3.11+."
  echo "Recreate the environment with Python 3.11 or newer before running verification."
  exit 1
fi

if [[ ! -d "client/node_modules" ]]; then
  echo "Error: client/node_modules not found."
  echo "Setup:"
  echo "  cd client"
  echo "  npm install"
  exit 1
fi

BACKEND_LOG="$(mktemp)"
FRONTEND_LOG="$(mktemp)"
trap 'rm -f "$BACKEND_LOG" "$FRONTEND_LOG"' EXIT

run_backend_tests() {
  set +e
  (
    source "$ROOT_DIR/.venv/bin/activate"
    cd "$ROOT_DIR/tests"
    pytest -q
  ) >"$BACKEND_LOG" 2>&1
  local rc=$?
  set -e
  cat "$BACKEND_LOG"
  return "$rc"
}

run_frontend_tests() {
  set +e
  (
    cd "$ROOT_DIR/client"
    npm test
  ) >"$FRONTEND_LOG" 2>&1
  local rc=$?
  set -e
  cat "$FRONTEND_LOG"
  return "$rc"
}

echo "Running backend tests..."
BACKEND_RC=0
run_backend_tests || BACKEND_RC=$?

echo "Running frontend tests..."
FRONTEND_RC=0
run_frontend_tests || FRONTEND_RC=$?

if [[ "$MODE" == "solved" ]]; then
  if [[ "$BACKEND_RC" -ne 0 || "$FRONTEND_RC" -ne 0 ]]; then
    echo
    echo "Solved verification failed: expected all tests to pass."
    exit 1
  fi
  echo
  echo "Solved verification passed: backend and frontend tests are green."
  exit 0
fi

if [[ "$BACKEND_RC" -eq 0 || "$FRONTEND_RC" -eq 0 ]]; then
  echo
  echo "Baseline verification failed: expected intentional failures in both suites."
  exit 1
fi

if grep -Eq "ERROR collecting|FastAPIError|ModuleNotFoundError" "$BACKEND_LOG"; then
  echo
  echo "Baseline verification failed: backend has collection/import issues."
  exit 1
fi

EXPECTED_BACKEND_FAILS=(
  "test_bug_a_status_filter_param_should_work"
  "test_bug_b_low_stock_should_include_equal_reorder_point"
  "test_bug_c_dashboard_should_return_camel_case_total_value"
  "test_feature_supplier_risk_endpoint_returns_risk_rows"
  "test_feature_orders_csv_export_returns_csv"
)

for test_name in "${EXPECTED_BACKEND_FAILS[@]}"; do
  if ! grep -q "$test_name" "$BACKEND_LOG"; then
    echo
    echo "Baseline verification failed: missing expected backend failure: $test_name"
    exit 1
  fi
done

EXPECTED_FRONTEND_FAILS=(
  "uses order_status query key when filtering orders"
  "returns supplier risk rows as an array payload"
  "clicking Export CSV triggers exportOrdersCsv"
)

for test_name in "${EXPECTED_FRONTEND_FAILS[@]}"; do
  if ! grep -q "$test_name" "$FRONTEND_LOG"; then
    echo
    echo "Baseline verification failed: missing expected frontend failure: $test_name"
    exit 1
  fi
done

echo
echo "Baseline verification passed: intentional failures detected with no infra blockers."
