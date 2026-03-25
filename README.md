# Codex Inventory Workshop Exercise

## Workshop Overview
This repository is a hands-on OpenAI Codex workshop project where participants practice two core capabilities:
1. Resolving real application defects with Codex.
2. Designing and implementing new product features with Codex.

The app is a lightweight inventory dashboard with a Vue frontend and FastAPI backend. It includes intentionally seeded issues and incomplete features for the lab.

## Learning Objectives
By the end of the workshop, participants should be able to:
- Diagnose failures with Codex using tests, logs, and targeted prompts.
- Apply iterative prompt loops to ship precise code fixes.
- Add API and UI functionality from a clear feature specification.
- Validate changes with backend and frontend tests.
- Explain tradeoffs and follow-up improvements in a debrief.

## Prereqs + Setup
### Prerequisites
- Node.js 20+
- Python 3.11+
- `pip` or `uv`

### Install + Run
```bash
# Backend dependencies
cd server
pip install -r requirements.txt

# Frontend dependencies
cd ../client
npm install

# Run backend (Terminal 1)
cd ../server
python main.py

# Run frontend (Terminal 2)
cd ../client
npm run dev
```

App URLs:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8001`
- API docs: `http://localhost:8001/docs`

### Run Tests
```bash
# Backend tests
cd tests
pytest

# Frontend tests
cd ../client
npm test
```

## Codex Workflow Primer
Use this loop for each task:
1. **Understand**: Ask Codex to explain current behavior and identify likely root causes.
2. **Constrain**: Provide exact failure symptoms and desired behavior.
3. **Patch**: Ask Codex for focused code changes (small diff, no unrelated refactors).
4. **Verify**: Run tests and app flow; ask Codex to interpret failures.
5. **Refine**: Repeat until acceptance criteria pass.

Prompt patterns:
- “Find why this test fails and propose minimal fix.”
- “Apply fix and keep API contract unchanged.”
- “Add tests first for this feature, then implement to green.”

## Exercise 1: Resolve Errors
Goal: use Codex to fix seeded defects.

### Seeded Bugs
- **Bug A**: frontend sends `status` query key while backend expects `order_status`.
- **Bug B**: low-stock logic counts `< reorder_point` but should count `<= reorder_point`.
- **Bug C**: dashboard response uses `total_value` but UI expects `totalValue`.

### Steps
1. Run backend tests:
   ```bash
   cd tests
   pytest backend/test_bug_regressions.py -q
   ```
2. Run frontend tests:
   ```bash
   cd client
   npm test
   ```
3. Use Codex to inspect failing tests and map each failure to root cause.
4. Implement fixes one-by-one; rerun tests after each change.
5. Confirm dashboard metrics and order filtering in browser.

### Hints
- Start with API contract mismatches before deeper logic changes.
- Keep naming conventions consistent across backend + frontend.
- Use test output as truth source; avoid speculative refactors.

### Expected Outcomes
- `tests/backend/test_bug_regressions.py` passes.
- Frontend API contract test for `order_status` passes.
- Dashboard correctly displays total value and low-stock count.

## Exercise 2: Add Features
Goal: use Codex to implement missing capabilities from specs.

### Feature 1: Supplier Lead Time Risk
Implement:
- `GET /api/risk/suppliers?warehouse=&category=`
- Aggregated payload shape:
  ```json
  {
    "supplier": "GridLite Power",
    "avg_lead_time_days": 33,
    "risk_level": "high",
    "affected_skus": ["PWR-404"]
  }
  ```
- Dashboard table population from this endpoint.

Acceptance criteria:
- Endpoint returns `200` and non-empty array.
- Each row has `supplier`, `avg_lead_time_days`, `risk_level`, `affected_skus`.
- Risk table renders on the dashboard.

### Feature 2: CSV Export for Filtered Orders
Implement:
- `GET /api/orders/export.csv`
- Respect active filters (`warehouse`, `category`, `order_status`, `month`).
- Wire “Export CSV” button to download a CSV file.

Acceptance criteria:
- Endpoint returns `text/csv` with header row.
- Export includes only rows matching active filters.
- UI button triggers actual export request.

### Steps
1. Make failing feature tests pass:
   - `tests/backend/test_feature_endpoints.py`
   - `client/src/__tests__/app.features.test.js`
2. Implement backend behavior first.
3. Wire frontend rendering and download behavior.
4. Validate manually in browser.

## Stretch Goals
- Add API alias support for both `status` and `order_status` with deprecation warning.
- Add loading/error states for dashboard cards and tables.
- Add pagination for orders.
- Add an E2E test (Playwright/Cypress) for filter + export flow.

## Debrief / Reflection Prompts
- Which Codex prompt patterns gave the best signal-to-noise ratio?
- What failure did tests catch that manual checks would likely miss?
- Where did API contracts drift, and how did you prevent recurrence?
- If productized, what logging/monitoring would you add next?

---

## 90-Minute Agenda
- **0:00-0:10** Intro, setup, repository orientation.
- **0:10-0:40** Exercise 1: resolve seeded errors.
- **0:40-1:15** Exercise 2: implement new features.
- **1:15-1:25** Test and manual validation pass.
- **1:25-1:30** Debrief and takeaways.
