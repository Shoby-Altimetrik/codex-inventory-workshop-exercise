#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage: ./scripts/reset_workshop_state.sh [--yes]

Restores workshop baseline files from HEAD and removes local workshop artifacts.
Use --yes to skip confirmation.
EOF
}

YES=0
if [[ "${1:-}" == "--yes" ]]; then
  YES=1
elif [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
elif [[ -n "${1:-}" ]]; then
  usage
  exit 1
fi

cd "$ROOT_DIR"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: must run inside a git repository."
  exit 1
fi

if [[ "$YES" -ne 1 ]]; then
  echo "This will discard local edits in core workshop files and remove local workshop artifacts."
  read -r -p "Continue? [y/N] " response
  if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
  fi
fi

BASELINE_FILES=(
  "README.md"
  "workshop-exercises.html"
  "client/src/App.vue"
  "client/src/api.js"
  "server/main.py"
  "tests/backend/test_bug_regressions.py"
  "tests/backend/test_feature_endpoints.py"
  "client/src/__tests__/api.contract.test.js"
  "client/src/__tests__/app.features.test.js"
  "docs/incidents/INC-2026-03-low-stock-kpi.md"
)

echo "Restoring baseline workshop files from HEAD..."
TRACKED_FILES=()
for file in "${BASELINE_FILES[@]}"; do
  if git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
    TRACKED_FILES+=("$file")
  fi
done

if [[ "${#TRACKED_FILES[@]}" -gt 0 ]]; then
  git restore --source=HEAD -- "${TRACKED_FILES[@]}"
fi

echo "Removing workshop artifacts and caches..."
rm -rf \
  .npm-cache \
  output \
  tests/.pytest_cache \
  client/.vitest \
  client/coverage \
  client/dist

find "$ROOT_DIR" -type d -name "__pycache__" -prune -exec rm -rf {} +
find "$ROOT_DIR" -type f -name "*.pyc" -delete

cat <<'EOF'

Workshop baseline reset complete.

Recommended next checks:
  1) python3 scripts/validate_guide_sync.py
  2) ./scripts/verify_workshop_state.sh --mode baseline

Expected baseline verification outcome:
  - Frontend test run reports 3 intentional failures.
  - Backend test run reports 5 intentional failures.
  - No backend collection/import errors.
EOF
