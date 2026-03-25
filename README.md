# Codex Inventory Workshop Exercise

## Workshop Overview
This workshop is designed to teach practical, repeatable workflows for using OpenAI Codex in a real codebase.

You will work through a full-stack app with:
- Vue frontend (`client/`)
- FastAPI backend (`server/`)
- Seeded tests and intentional defects (`tests/`, `client/src/__tests__/`)

Workshop goals:
1. Install and configure Codex successfully (App or CLI).
2. Use Codex to diagnose and fix real defects.
3. Use Codex to add net-new functionality with test validation.
4. Use Playwright CLI skill to validate and iterate on a UI feature.

Recommended branch strategy:
- Start on `main` for workshop exercises.
- Use feature branches for participant submissions or instructor review.

---

## Learning Objectives
By the end of the workshop, participants should be able to:
- Install Codex (App or CLI) and connect it to a local repository.
- Prompt Codex to map architecture, identify failure roots, and generate targeted diffs.
- Resolve backend/frontend contract drift safely.
- Add backend and frontend features from acceptance criteria.
- Validate behavior with automated tests and browser automation.

---

## Prereqs + Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- `pip` (or `uv`)
- ChatGPT sign-in or OpenAI API key for Codex authentication

### Clone and install dependencies
```bash
# clone your workshop repo
git clone <your-repo-url>
cd codex-inventory-workshop-exercise

# backend setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
pip install pytest httpx

# frontend setup
cd client
npm install
cd ..
```

### Run the app
Use two terminals.

Terminal 1 (backend):
```bash
source .venv/bin/activate
cd server
python main.py
```

Terminal 2 (frontend):
```bash
cd client
npm run dev
```

### Local URLs
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8001`
- API docs: `http://localhost:8001/docs`

### Test commands
Backend:
```bash
source .venv/bin/activate
cd tests
pytest -q
```

Frontend:
```bash
cd client
npm test
```

---

## Codex Workflow Primer
Use this loop in every exercise.

1. Orient
- Ask Codex for relevant files and data flow first.
- Example: `Trace order_status from UI controls to backend query filtering.`

2. Reproduce
- Run tests or UI flow and capture exact failure output.

3. Constrain
- Ask for smallest viable fix with no unrelated refactors.

4. Verify
- Re-run tests immediately.
- Re-check manual behavior in browser.

5. Summarize
- Ask Codex for a short changelog, risks, and follow-up hardening ideas.

Prompt patterns:
- `Find root cause from this failing test output and propose a minimal patch.`
- `Keep API contract stable and update only what is needed.`
- `Add or update tests first, then implement.`

---

## Exercise 1: Install Codex (App or CLI) and Connect Project (10-20 minutes)
Goal: everyone can run Codex locally against this repository using either UI or terminal workflow.

Official guides:
- ChatGPT Codex get-started: [https://chatgpt.com/codex/get-started](https://chatgpt.com/codex/get-started)
- Codex App docs: [https://developers.openai.com/codex/app](https://developers.openai.com/codex/app)
- Codex CLI quickstart (official repo): [https://github.com/openai/codex](https://github.com/openai/codex)

### Option A: Codex App path
1. Open Codex app and sign in with your ChatGPT account.
2. Select this local folder/repository.
3. Kick off your first task prompt.
4. Run these orientation prompts:
   - `Summarize repository structure.`
   - `List intentionally failing tests and their purpose.`
   - `Map dashboard summary data from backend to UI.`

### Option B: Codex CLI path
1. Install Codex CLI:
   ```bash
   npm install -g @openai/codex
   # or
   brew install --cask codex
   ```
2. Start Codex in this repo:
   ```bash
   codex
   ```
3. Sign in with ChatGPT (recommended) or API key.
4. Run the same three orientation prompts from Option A.

### Done when
- Participant can run Codex via App or CLI.
- Codex returns accurate file paths and behavior summary.
- Participant can issue prompts and iterate in local mode.

---

## Exercise 2: Bug Fix A - Query Parameter Contract (10-20 minutes)
Goal: fix status filter mismatch between frontend and backend contracts.

### Problem
Frontend sends `status`, while backend primarily uses `order_status`.

### Steps
1. Checkout workshop baseline:
   ```bash
   git checkout main
   ```
2. Run frontend tests:
   ```bash
   cd client
   npm test
   ```
3. Find failing API contract test.
4. Use Codex to patch query param mapping.
5. Re-run tests and verify status filtering in UI.

### Acceptance criteria
- Frontend contract test for `order_status` passes.
- Filtering by `Processing` or `Backordered` returns correct rows.

---

## Exercise 3: Bug Fix B - Low Stock Business Rule (10-20 minutes)
Goal: fix low-stock calculation logic.

### Problem
Low-stock count uses `< reorder_point` instead of `<= reorder_point`.

### Steps
1. Run backend regression tests:
   ```bash
   source .venv/bin/activate
   cd tests
   pytest backend/test_bug_regressions.py -q
   ```
2. Use Codex to locate low-stock calculation.
3. Apply minimal fix.
4. Re-run test file.

### Acceptance criteria
- `lowStockCount` includes items exactly at reorder point.
- Backend regression test for Bug B passes.

---

## Exercise 4: Bug Fix C - Response Field Naming Drift (10-20 minutes)
Goal: align API payload with frontend expectations.

### Problem
Dashboard response returns `total_value` while UI expects `totalValue`.

### Steps
1. Reproduce failing dashboard metric behavior.
2. Use Codex to trace response contract.
3. Fix naming mismatch with minimal blast radius.
4. Re-run frontend and backend regression tests.

### Acceptance criteria
- Dashboard shows total value correctly.
- Regression tests for Bug C pass.

---

## Exercise 5: Feature A - Supplier Lead Time Risk API + UI (10-20 minutes)
Goal: implement a full-stack feature from endpoint to table rendering.

### Build
- API endpoint: `GET /api/risk/suppliers?warehouse=&category=`
- Response shape per row:
  - `supplier`
  - `avg_lead_time_days`
  - `risk_level`
  - `affected_skus`
- Dashboard should render returned rows.

### Steps
1. Run feature endpoint tests:
   ```bash
   source .venv/bin/activate
   cd tests
   pytest backend/test_feature_endpoints.py -q
   ```
2. Use Codex to implement backend aggregation and risk bucketing.
3. Update frontend fetch/render behavior.
4. Re-run backend + frontend tests.

### Acceptance criteria
- Endpoint returns `200` and non-empty array.
- Payload matches required shape.
- Supplier risk table renders in dashboard.

---

## Exercise 6: Feature B - CSV Export for Filtered Orders (10-20 minutes)
Goal: implement export functionality that honors active filters.

### Build
- API endpoint: `GET /api/orders/export.csv`
- Include filters: `warehouse`, `category`, `order_status`, `month`
- Wire `Export CSV` button to trigger export behavior.

### Steps
1. Run failing feature tests (backend and frontend).
2. Use Codex to implement backend CSV output and content headers.
3. Use Codex to wire frontend export trigger.
4. Verify generated CSV content matches active filters.

### Acceptance criteria
- Endpoint returns `text/csv` with header row.
- Filtered export data is correct.
- Export trigger test passes.

---

## Exercise 7: Playwright CLI Skill Feature - Add Orders Search UX (10-20 minutes)
Goal: add a UI feature and validate it using the Playwright CLI skill workflow.

### Feature to add
Add a client-side `Order Search` input in the Orders section that filters visible orders by:
- order id
- customer
- status

### Why Playwright here
This feature is interaction-heavy and ideal for browser automation validation:
- typing into a real input
- checking list changes
- verifying no regressions in Apply Filters flow

### Playwright CLI skill setup
Use the Playwright skill wrapper flow.

Prerequisite check:
```bash
command -v npx >/dev/null 2>&1
```

Set helper path:
```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"
```

### Playwright validation flow
```bash
"$PWCLI" open http://localhost:3000 --headed
"$PWCLI" snapshot
# click/typing refs will vary by snapshot, use returned e* ids
"$PWCLI" type eX "ORD-5002"
"$PWCLI" snapshot
"$PWCLI" screenshot
```

Recommended checks:
- Searching `ORD-5002` leaves only that order visible.
- Clearing search restores full list.
- Existing Apply Filters behavior still works after adding search.

### Acceptance criteria
- New search input exists and filters orders in real time.
- Behavior validated manually and with Playwright CLI interaction.
- No existing tests regress.

---

## Stretch Goals
- Add deprecation warning support for `status` alias usage in backend logs.
- Add loading and error states for all async dashboard sections.
- Add sorting and pagination controls for orders.
- Add Playwright smoke script snippets for critical paths.

---

## Debrief / Reflection Prompts
- Which prompts produced the highest-confidence code edits?
- Which failures were easiest to localize and why?
- Which checks from Playwright caught issues unit tests did not?
- Where did API contracts drift, and how can your team prevent that?
- What would you productionize next (observability, rollout, safety)?

---

## Agenda (10-20 Minutes Per Segment)
- Exercise 1: install Codex (App or CLI) and connect local project. (10-20 minutes)
- Exercise 2: Bug Fix A (`status` vs `order_status`). (10-20 minutes)
- Exercise 3: Bug Fix B (low stock rule). (10-20 minutes)
- Exercise 4: Bug Fix C (`total_value` vs `totalValue`). (10-20 minutes)
- Exercise 5: Feature A (supplier risk endpoint + UI). (10-20 minutes)
- Exercise 6: Feature B (CSV export). (10-20 minutes)
- Exercise 7: Playwright feature and validation. (10-20 minutes)
- Debrief and recap. (10-20 minutes)
