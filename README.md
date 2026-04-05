# Altimetrik Codex Inventory Workshop Exercise

## Workshop Overview
This Altimetrik workshop is designed to teach practical, repeatable workflows for using OpenAI Codex in a real codebase.

You will work through a full-stack app with:
- Vue frontend (`client/`)
- FastAPI backend (`server/`)
- Seeded tests and intentional defects (`tests/`, `client/src/__tests__/`)

Workshop goals:
1. Install and configure Codex successfully (App or CLI).
2. Establish durable repo context and a repeatable verification loop.
3. Use Codex to diagnose and fix real defects.
4. Use Codex to add net-new functionality with spec-first validation.
5. Use skills, MCP-style tooling, and review workflows intentionally.

Workshop baseline model:
- `main` is the canonical workshop baseline (intentionally failing in expected places).
- Do workshop-development and facilitator improvements on a review branch, not on `main`.
- Use `./scripts/reset_workshop_state.sh --yes` before each delivery run.
- Use `./scripts/verify_workshop_state.sh --mode baseline` to confirm expected baseline behavior.

## Why Codex Here
- Full-stack tracing from UI to API to tests in one loop.
- Constrained patch generation focused on minimal blast radius.
- Repo-native instructions via [`AGENTS.md`](AGENTS.md) keep project context visible to Codex.
- Verification-first workflow combines tests, browser checks, and screenshot evidence.
- Skills and MCP-style tooling make it easy to show when Codex should reach beyond local file edits.
- Review branches keep facilitator improvements separate from the workshop baseline.
- Practical operator controls for repeatable workshop delivery.

## Client Outcomes
By completion, participants can transfer these capabilities to their own codebases:
- Exercise 1: stand up Codex App/CLI workflow against a local repo.
- Exercise 2: diagnose and fix frontend/backend query-contract drift safely.
- Exercise 3: run incident-style KPI triage, implement a fix, and document RCA.
- Exercise 4: stabilize naming contracts across service and UI layers.
- Exercise 5: implement a scoped API + UI feature with acceptance-driven tests.
- Exercise 6: ship export/reporting behavior tied to live filter state.
- Exercise 7: validate interactive UX behavior with browser automation.
- Exercise 8: execute visual QA with reproducible screenshot evidence.
- Exercise 9: design and deliver a stakeholder-facing operations dashboard slice.
- Exercise 10: internationalize UI flows for multilingual team adoption.

---

## Learning Objectives
By the end of the workshop, participants should be able to:
- Install Codex (App or CLI) and connect it to a local repository.
- Establish project context with repo instructions and artifact templates.
- Prompt Codex to map architecture, identify failure roots, and generate targeted diffs.
- Create or approve a short spec before implementing a feature.
- Resolve backend/frontend contract drift safely.
- Add backend and frontend features from acceptance criteria.
- Validate behavior with automated tests, browser automation, and visual evidence.

---

## Prereqs + Setup

### Prerequisites
- Node.js 20+
- Python 3.11+
- `pip` (or `uv`)
- ChatGPT sign-in or OpenAI API key for Codex authentication

Important note for macOS participants:
- The system `python3` command may still point to Python 3.9.
- This workshop uses Python 3.11+ syntax in the FastAPI app.
- If baseline verification fails before tests run, check `python --version` inside `.venv`.

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

### Create a review branch
Keep your work isolated so the workshop baseline remains reviewable.

```bash
git checkout -b codex/<your-workshop-branch>
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

Or use the helper script:
```bash
./scripts/start.sh
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

### Workshop baseline controls
Reset to canonical baseline:
```bash
./scripts/reset_workshop_state.sh --yes
```

Verify baseline (intentional failures only):
```bash
./scripts/verify_workshop_state.sh --mode baseline
```

Verify solved state (all tests green after workshop completion):
```bash
./scripts/verify_workshop_state.sh --mode solved
```

Validate README/HTML alignment:
```bash
python3 scripts/validate_guide_sync.py
```

Delivery preflight checklist:
- Run `python3 scripts/validate_guide_sync.py`.
- Run `./scripts/verify_workshop_state.sh --mode baseline`.
- Confirm repo is clean (`git status --short`).
- Confirm app boot commands still use `localhost:3000` and `localhost:8001`.

CI coverage:
- `.github/workflows/workshop-preflight.yml` runs guide sync validation and baseline verification on push/PR.

---

## Codex Workflow Primer
Use this loop in every exercise.

1. Orient
- Ask Codex for relevant files and data flow first.
- Example: `Trace order_status from UI controls to backend query filtering.`

2. Set context
- Inspect [`AGENTS.md`](AGENTS.md) before substantial changes.
- Keep workshop deliverables in `output/`.
- Call out whether you are preserving the baseline or implementing the exercise.

3. Reproduce
- Run tests or UI flow and capture exact failure output.

4. Plan
- For feature work, create or approve a short spec before editing.
- Use [`output/spec.md`](output/spec.md) when the exercise asks for a design artifact.

5. Constrain
- Ask for smallest viable fix with no unrelated refactors.

6. Verify
- Re-run tests immediately.
- Re-check manual behavior in browser.
- Save screenshots or notes when the exercise asks for proof.

7. Summarize
- Ask Codex for a short changelog, risks, and follow-up hardening ideas.

Prompt patterns:
- `Find root cause from this failing test output and propose a minimal patch.`
- `Before coding, draft a concise implementation plan and acceptance criteria.`
- `Keep API contract stable and update only what is needed.`
- `Add or update tests first, then implement.`

## Project Context + Artifacts
Codex works best when the repo carries its own instructions and expected outputs.

- [`AGENTS.md`](AGENTS.md): shared project guidance for Codex sessions
- [`output/architecture-overview.md`](output/architecture-overview.md): early repo-understanding artifact
- [`output/spec.md`](output/spec.md): plan-first feature artifact
- [`output/incident-rca.md`](output/incident-rca.md): incident response artifact
- [`output/screenshots/`](output/screenshots/): visual QA evidence

Additional workshop support docs:
- [`docs/codex/mcp-playwright.md`](docs/codex/mcp-playwright.md)
- [`docs/codex/secrets-and-config.md`](docs/codex/secrets-and-config.md)
- [`docs/codex/review-workflow.md`](docs/codex/review-workflow.md)

---

## Exercise 1: Install Codex (App or CLI) and Connect Project (10-20 minutes)
Goal: connect Codex to the repo, create an isolated review branch, establish repo context, and generate an early architecture artifact.

Official guides:
- ChatGPT Codex get-started: [https://chatgpt.com/codex/get-started](https://chatgpt.com/codex/get-started)
- Codex App docs: [https://developers.openai.com/codex/app](https://developers.openai.com/codex/app)
- Codex CLI quickstart (official repo): [https://github.com/openai/codex](https://github.com/openai/codex)

### Option A: Codex App path
1. Open Codex app and sign in with your ChatGPT account.
2. Select this local folder/repository.
3. Create a review branch in your terminal:
   ```bash
   git checkout -b codex/<your-workshop-branch>
   ```
4. Kick off your first task prompt.
5. Run these orientation prompts:
   - `Read AGENTS.md and summarize the project rules I should follow.`
   - `Create an architecture overview of this repository and save it to output/architecture-overview.md.`
   - `Tell me which tests are intentionally failing on the workshop baseline and why.`
   - `Start the backend and frontend locally and tell me how to verify they are running.`
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
4. Create a review branch:
   ```bash
   git checkout -b codex/<your-workshop-branch>
   ```
5. Run the same orientation prompts from Option A.

### Expected outputs
- Review branch exists and is not `main`.
- `output/architecture-overview.md` is updated with a repo map and main flows.
- Participant can explain how the app starts and how the intentional baseline works.

### Acceptance criteria
- Participant can run Codex via App or CLI.
- Codex returns accurate file paths, constraints, and architecture summary.
- Participant has a review branch plus an architecture artifact.
- Participant can issue prompts and iterate in local mode.

---

## Exercise 2: Bug Fix A - Query Parameter Contract (10-20 minutes)
Goal: fix status filter mismatch between frontend and backend contracts.

### Problem
Frontend sends `status`, while backend primarily uses `order_status`.

### Codex setup for this exercise
- Codex App path:
  1. Open this repo in Codex App (or reuse the session from Exercise 1).
  2. Use this prompt:
     - `Fix Bug A: frontend sends status but backend expects order_status. Find the failing test, apply a minimal patch, and re-run affected tests.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

### Steps
1. Reset to workshop baseline:
   ```bash
   ./scripts/reset_workshop_state.sh --yes
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

## Exercise 3: Incident Response - Low Stock KPI Mismatch (10-20 minutes)
Goal: triage and resolve a production-style KPI mismatch affecting planning decisions.

### Incident brief
- A planning report understated low-stock exposure and triggered a data-quality escalation.
- See incident packet: `docs/incidents/INC-2026-03-low-stock-kpi.md`.
- Working hypothesis: low-stock logic uses `< reorder_point` instead of `<= reorder_point`.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Treat this as incident response: validate low-stock KPI mismatch evidence, apply minimal fix for reorder-point equality, rerun regressions, and summarize RCA.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

### Steps
1. Read incident packet and identify impacted KPI behavior.
2. Run backend regression tests:
   ```bash
   source .venv/bin/activate
   cd tests
   pytest backend/test_bug_regressions.py -q
   ```
3. Use Codex to locate low-stock calculation and patch with minimal blast radius.
4. Re-run regression tests and confirm KPI correction.
5. Capture a short RCA + mitigation note (3-5 bullets) in `output/incident-rca.md`.

### Acceptance criteria
- `lowStockCount` includes items exactly at reorder point.
- Backend regression test for this KPI incident passes.
- `output/incident-rca.md` exists with root cause + mitigation bullets.

---

## Exercise 4: Bug Fix C - Response Field Naming Drift (10-20 minutes)
Goal: align API payload with frontend expectations.

### Problem
Dashboard response returns `total_value` while UI expects `totalValue`.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Fix Bug C: total value field name drift between backend and UI. Keep contract stable, make minimal change, and re-run regression tests.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

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

### Plan-first artifact
Before implementing, create or update [`output/spec.md`](output/spec.md) with:
- the problem statement
- acceptance criteria
- backend/frontend/test changes
- verification plan

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Before coding, draft a concise spec in output/spec.md for Feature A. Then implement GET /api/risk/suppliers with warehouse/category filters, render supplier risk rows in dashboard, and update tests.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

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
2. Draft or approve `output/spec.md`.
3. Use Codex to implement backend aggregation and risk bucketing.
4. Update frontend fetch/render behavior.
5. Re-run backend + frontend tests.

### Acceptance criteria
- Endpoint returns `200` and non-empty array.
- Payload matches required shape.
- Supplier risk table renders in dashboard.
- `output/spec.md` reflects the accepted implementation plan.

---

## Exercise 6: Feature B - CSV Export for Filtered Orders (10-20 minutes)
Goal: implement export functionality that honors active filters.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Implement Feature B: add GET /api/orders/export.csv honoring active filters and wire Export CSV button in UI. Add/update tests.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

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

## Skills Primer
Skills are reusable task guides that help Codex apply a workflow consistently. In this workshop:

- the repo ships a sample skill at [`.codex/skills/workshop-evidence/SKILL.md`](.codex/skills/workshop-evidence/SKILL.md)
- Exercises 7-8 use skills to make QA and evidence capture repeatable
- the lesson is not “use more instructions”; it is “package a useful workflow once and reuse it”

Try this prompt before Exercise 7:
- `Read .codex/skills/workshop-evidence/SKILL.md and explain when this skill should be used in this repo.`

## MCP Primer
Model Context Protocol (MCP) gives Codex access to tools beyond local file editing. In this workshop, browser automation is the key example because it validates interactive behavior that unit tests may not fully capture.

- primer doc: [`docs/codex/mcp-playwright.md`](docs/codex/mcp-playwright.md)
- use browser tooling when the problem is interactive
- keep tool usage evidence-driven: snapshots, screenshots, and concise verification notes

## Exercise 7: Playwright CLI Skill Feature - Add Orders Search UX (10-20 minutes)
Goal: add a UI feature and validate it using the Playwright CLI skill workflow.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Add Order Search UX in orders view (id, customer, status) and validate behavior with Playwright CLI snapshots and screenshots.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

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
- Save browser notes, snapshots, or screenshots under `output/playwright/` when possible.

### Acceptance criteria
- New search input exists and filters orders in real time.
- Behavior validated manually and with Playwright CLI interaction.
- Browser evidence is saved or summarized for review.
- No existing tests regress.

---

## Exercise 8: Screenshot Capture Skill - Final Visual QA (10-20 minutes)
Goal: use Screenshot Capture to visually validate that all built work is correct and present.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Run final visual QA with screenshot capture. Produce captures for KPI correctness, supplier risk table, order search, and export controls.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

### Why this exercise matters
Automated tests and browser flows are necessary but still miss visual regressions. This step creates a repeatable visual QA pass for workshop deliverables.

### Screenshot skill setup
```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export SS_SKILL="$CODEX_HOME/skills/screenshot"
```

macOS permission preflight:
```bash
bash "$SS_SKILL/scripts/ensure_macos_permissions.sh"
```

### Validation checklist
Capture screenshots for each required state:
1. Dashboard with corrected KPI values (including total value).
2. Supplier risk table visible with populated rows.
3. Orders view with search input filtering results.
4. Export CSV control visible in Orders view.
5. Optional: add a short handoff note using `docs/templates/reviewer-summary-template.md`.

### Example capture commands
Capture the currently focused window to temp:
```bash
python3 "$SS_SKILL/scripts/take_screenshot.py" --mode temp --active-window
```

Capture a specific browser app window (macOS):
```bash
python3 "$SS_SKILL/scripts/take_screenshot.py" --mode temp --app "Google Chrome"
```

Capture to a saved artifacts folder:
```bash
mkdir -p output/screenshots
python3 "$SS_SKILL/scripts/take_screenshot.py" --path output/screenshots/final-validation.png
```

### Acceptance criteria
- Screenshots exist for all required validation states.
- No obvious visual regressions (missing components, layout collapse, unreadable UI).
- Evidence artifacts are saved for review.

---

## Review And Advanced Workflows
By this point, participants should be able to package work for review without touching the workshop baseline on `main`.

Review workflow notes:
- keep changes on a review branch
- summarize what remains intentionally broken
- separate baseline hardening from curriculum/content edits when possible
- use [`docs/templates/reviewer-summary-template.md`](docs/templates/reviewer-summary-template.md) as a reviewer checklist

Optional advanced follow-ons:
- isolated branches or git worktrees for experimentation
- parallel agent investigation on bounded tasks
- future GitHub review automation once the core workshop flow is approved

## Exercise 9: Feature C - Add Operations Dashboard View (10-20 minutes)
Goal: add a focused dashboard view that gives operations leaders a quick demand-vs-spend signal. Optional follow-on exercise for this delivery phase.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Add an Operations Dashboard view using existing demand and spending APIs. Implement a concise KPI summary + supporting table/card section and add tests.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

### Build
- Add a new dashboard section (or routed view) for operations health.
- Use existing backend endpoints:
  - `GET /api/demand`
  - `GET /api/spending`
- Show at least:
  - one computed KPI summary
  - one supporting detail table/list
  - one clear signal state (e.g., stable/increasing/decreasing)

### Steps
1. Define the UI contract for the operations dashboard section.
2. Use Codex to implement data loading and derived KPI computation.
3. Add render logic and any required component/test updates.
4. Re-run frontend tests and manually verify the new section in browser.

### Acceptance criteria
- Operations dashboard section is visible and populated from live API data.
- Derived KPI/signal values are deterministic for seeded data.
- Frontend tests for the new dashboard behavior pass.

---

## Exercise 10: Feature D - Multilingual UI (English + Spanish) (10-20 minutes)
Goal: make the workshop app usable in at least two languages with a clean translation pattern. Optional follow-on exercise for this delivery phase.

### Codex setup for this exercise
- Codex App path:
  1. Reuse the same repo session in Codex App.
  2. Use this prompt:
     - `Add multilingual support (English and Spanish): language selector, translation dictionary, UI label wiring, and tests for language toggle behavior.`
- Codex CLI path:
  1. Start or return to Codex in this repo:
     ```bash
     codex
     ```
  2. Use the same prompt as the App path.

### Build
- Add a language selector in the UI (`en`, `es`).
- Externalize visible UI strings into a translation map/object.
- Persist selected language (for example in `localStorage`).
- Default/fallback language should remain English.

### Steps
1. Identify all user-facing labels used in current app sections.
2. Use Codex to create translation structure and selector wiring.
3. Apply translations across dashboard, filters, and table headers.
4. Add/update tests for language toggle and fallback behavior.

### Acceptance criteria
- Users can switch between English and Spanish at runtime.
- Key labels update without a page reload.
- Language preference persists across refresh.
- Translation-related tests pass.

---

## Stretch Goals
- Use a git worktree or isolated branch to prototype an optional enhancement.
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
- Exercise 1: install Codex, create a review branch, set repo context, and generate architecture notes. (10-20 minutes)
- Exercise 2: Bug Fix A (`status` vs `order_status`). (10-20 minutes)
- Exercise 3: incident response for low-stock KPI mismatch. (10-20 minutes)
- Exercise 4: Bug Fix C (`total_value` vs `totalValue`). (10-20 minutes)
- Exercise 5: Feature A with plan-first spec (`output/spec.md`). (10-20 minutes)
- Exercise 6: Feature B (CSV export). (10-20 minutes)
- Exercise 7: Playwright feature and validation. (10-20 minutes)
- Exercise 8: Screenshot Capture final visual QA. (10-20 minutes)
- Exercise 9: operations dashboard view. (optional follow-on)
- Exercise 10: multilingual UI (English + Spanish). (optional follow-on)
- Debrief and recap. (10-20 minutes)
