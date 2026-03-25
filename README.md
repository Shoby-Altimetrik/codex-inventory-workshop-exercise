# Codex Inventory Workshop Exercise

## Workshop Overview
Welcome to a hands-on OpenAI Codex workshop built around a realistic full-stack application. This project is designed to help learners move beyond “toy prompts” and practice the actual day-to-day workflow of using Codex to understand code, diagnose defects, implement changes, and validate outcomes.

This repository includes:
- A Vue frontend (`client/`)
- A FastAPI backend (`server/`)
- Automated tests for both seeded defects and feature work (`tests/`, `client/src/__tests__/`)
- A baseline branch with intentional issues (`main`)
- An instructor solution branch with completed fixes (`codex-instructor-solution`)

Primary workshop outcomes:
1. Get participants fully set up with the Codex app and working in a local project.
2. Practice structured debugging and feature delivery with Codex in a controlled scenario.

---

## Learning Objectives
By the end of the workshop, participants should be able to:
- Install and configure the Codex app for local repository work.
- Use Codex prompts to inspect architecture, trace failures, and generate focused patches.
- Resolve API/UI contract drift with test-guided debugging.
- Implement new backend and frontend features from acceptance criteria.
- Validate changes with backend and frontend tests before shipping.
- Reflect on prompt quality, verification habits, and implementation tradeoffs.

---

## Prereqs + Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- `pip` (or `uv`)
- A ChatGPT account or OpenAI API key for Codex sign-in

### Clone and install dependencies
```bash
# from your parent projects directory
git clone <your-repo-url>
cd codex-inventory-workshop-exercise

# backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r server/requirements.txt
pip install pytest httpx

# frontend
cd client
npm install
cd ..
```

### Run the app locally
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

### Run tests
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
Use this loop repeatedly in each exercise:

1. **Orient**
   - Ask Codex for a quick map of the relevant files and data flow.
   - Example: “Trace how order status filter moves from UI to API query params.”

2. **Observe failure**
   - Run tests or reproduce manually.
   - Share exact failing output with Codex.

3. **Constrain the task**
   - Ask for minimal, high-confidence edits only.
   - Example: “Fix this failing test without broad refactors.”

4. **Patch and verify**
   - Apply one logical change at a time.
   - Re-run tests immediately after each fix.

5. **Summarize and lock in**
   - Ask Codex for a short changelog and risk review.
   - Confirm acceptance criteria explicitly.

Prompt patterns that work well:
- “Explain root cause from this stack trace and file references.”
- “Propose smallest patch that makes this test pass.”
- “List edge cases this change could break.”
- “Write/adjust tests first, then implement.”

---

## Exercise 1: Install Codex App and Connect to the Project
Goal: ensure every participant can run Codex locally against this codebase.

Official reference:
- OpenAI Codex app guide: [https://developers.openai.com/codex/app](https://developers.openai.com/codex/app)

### What participants should complete
1. Install the Codex app from the official guide.
2. Open Codex and sign in (ChatGPT account or API key).
3. Select this project folder in Codex.
4. Confirm Codex is in **Local** mode for this repository.
5. Send your first project message in Codex.

### Suggested first messages
- “Summarize this repository structure and key entry points.”
- “Which tests are designed to fail in the baseline branch and why?”
- “Show me the backend endpoints used by the dashboard.”

### Verification checklist
- Codex opens this repository and can read files.
- Codex can answer architecture questions with correct paths.
- Participant can issue one actionable prompt and receive a useful result.

### Troubleshooting tips
- If project files appear empty, confirm the selected folder path.
- If auth fails, sign out/in again and re-open the project.
- If local execution tools are unavailable, verify OS permissions for terminal/shell access.

---

## Exercise 2: Resolve Seeded Errors with Codex
Goal: use Codex + tests to fix intentionally seeded defects.

### Seeded defects
- **Bug A**: frontend sends `status` while backend historically expected `order_status`.
- **Bug B**: low-stock logic used `< reorder_point` instead of `<= reorder_point`.
- **Bug C**: dashboard response used `total_value` while UI expected `totalValue`.

### Steps
1. Start from the baseline branch:
   ```bash
   git checkout main
   ```
2. Run backend regression tests:
   ```bash
   source .venv/bin/activate
   cd tests
   pytest backend/test_bug_regressions.py -q
   ```
3. Run frontend contract tests:
   ```bash
   cd ../client
   npm test
   ```
4. Use Codex to map each failure to exact files and minimal fixes.
5. Apply one fix at a time and re-run tests after each patch.

### Hints
- Prioritize contract mismatches first (query keys, response field names).
- Use test failure text as the source of truth, not assumptions.
- Keep naming consistent across backend return values and frontend consumers.

### Expected outcomes
- Backend bug regression tests pass.
- Frontend API contract tests pass.
- Dashboard metrics and status filtering behave correctly.

---

## Exercise 3: Add New Features with Codex
Goal: use Codex to deliver missing features from product-style acceptance criteria.

### Feature 1: Supplier Lead Time Risk
Implement:
- `GET /api/risk/suppliers?warehouse=&category=`
- Response rows with:
  - `supplier`
  - `avg_lead_time_days`
  - `risk_level`
  - `affected_skus`
- Render supplier risk data in dashboard table.

Acceptance criteria:
- Endpoint returns `200` and non-empty array.
- Payload shape matches contract.
- Risk table renders and updates from API data.

### Feature 2: CSV Export for Filtered Orders
Implement:
- `GET /api/orders/export.csv`
- Respect active filters (`warehouse`, `category`, `order_status`, `month`).
- Wire **Export CSV** button to trigger real export flow.

Acceptance criteria:
- Endpoint returns `text/csv` with header row.
- Exported rows match active filters.
- UI action invokes export behavior successfully.

### Steps
1. Run failing feature tests:
   - `tests/backend/test_feature_endpoints.py`
   - `client/src/__tests__/app.features.test.js`
2. Implement backend first, then frontend integration.
3. Re-run all tests.
4. Verify behavior manually in browser.

---

## Stretch Goals
- Add deprecation messaging for `status` vs `order_status` alias behavior.
- Add loading and error states for all dashboard cards/tables.
- Add pagination and sort controls to orders list.
- Add end-to-end test coverage for filter + export flow.
- Add a short architectural decision record describing final API contract choices.

---

## Debrief / Reflection Prompts
Use these to close the workshop:
- Which prompt formats produced the fastest high-confidence fixes?
- Which bug took the longest and why?
- Which tests prevented regressions you would likely miss manually?
- What would you improve in prompt hygiene for future sessions?
- If this were production, what observability and rollback steps would you add?

---

## 90-Minute Agenda
- **0:00–0:10** Intro, goals, repository orientation.
- **0:10–0:25** Exercise 1: install Codex app and connect local project.
- **0:25–0:50** Exercise 2: resolve seeded defects.
- **0:50–1:20** Exercise 3: implement new features.
- **1:20–1:27** Full test and manual validation pass.
- **1:27–1:30** Debrief and takeaways.
