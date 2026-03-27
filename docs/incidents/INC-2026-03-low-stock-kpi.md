# INC-2026-03: Low-Stock KPI Mismatch

## Incident Brief
- **Date opened:** March 24, 2026
- **Severity:** SEV-2 (planning-impacting metric error)
- **Impacted teams:** Procurement, Supply Planning, Ops Analytics
- **Customer-facing impact:** A planning report sent to enterprise buyers understated low-stock exposure.

## Symptoms
- Dashboard card shows `lowStockCount=2` for `warehouse=all` and `category=all`.
- Ops reconciliation sheet and planner audit both expect `lowStockCount=3`.
- SKU `SNS-020` (quantity equals reorder point) is not counted as low-stock.

## Evidence Snippets
- API check:
  - `GET /api/dashboard/summary` returns `lowStockCount: 2`.
- Data check:
  - `server/data/inventory.json` includes `SNS-020` with `quantity=30` and `reorder_point=30`.
- Regression signal:
  - `tests/backend/test_bug_regressions.py::test_bug_b_low_stock_should_include_equal_reorder_point` fails.

## Investigation Hypothesis
Low-stock KPI currently uses strict less-than (`quantity < reorder_point`) while business policy treats equality as low-stock (`quantity <= reorder_point`).

## Workshop Deliverable
During Exercise 3, produce a short RCA note including:
1. Root cause.
2. Why tests missed/prevented drift.
3. Mitigation (test coverage + acceptance guardrail).
