from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def load_json(name: str) -> list[dict[str, Any]]:
    with (DATA_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


app = FastAPI(title="Codex Inventory Workshop API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Codex Inventory Workshop API", "version": "0.1.0"}


@app.get("/api/inventory")
def get_inventory(
    warehouse: str | None = Query(default=None),
    category: str | None = Query(default=None),
) -> list[dict[str, Any]]:
    rows = load_json("inventory.json")
    if warehouse and warehouse.lower() != "all":
        rows = [r for r in rows if r["warehouse"].lower() == warehouse.lower()]
    if category and category.lower() != "all":
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    return rows


@app.get("/api/orders")
def get_orders(
    warehouse: str | None = Query(default=None),
    category: str | None = Query(default=None),
    order_status: str | None = Query(default=None),
    month: str | None = Query(default=None),
) -> list[dict[str, Any]]:
    rows = load_json("orders.json")
    if warehouse and warehouse.lower() != "all":
        rows = [r for r in rows if r["warehouse"].lower() == warehouse.lower()]
    if category and category.lower() != "all":
        rows = [r for r in rows if r["category"].lower() == category.lower()]
    if order_status and order_status.lower() != "all":
        rows = [r for r in rows if r["status"].lower() == order_status.lower()]
    if month and month.lower() != "all":
        rows = [r for r in rows if r["month"] == month]

    for row in rows:
        row["total_value"] = sum(i["quantity"] * i["unit_price"] for i in row["items"])
    return rows


@app.get("/api/demand")
def get_demand() -> list[dict[str, Any]]:
    return load_json("demand.json")


@app.get("/api/spending")
def get_spending() -> list[dict[str, Any]]:
    return load_json("spending.json")


@app.get("/api/dashboard/summary")
def dashboard_summary(
    warehouse: str | None = Query(default=None),
    category: str | None = Query(default=None),
    order_status: str | None = Query(default=None),
    month: str | None = Query(default=None),
) -> dict[str, Any]:
    inventory = get_inventory(warehouse=warehouse, category=category)
    orders = get_orders(
        warehouse=warehouse,
        category=category,
        order_status=order_status,
        month=month,
    )

    # BUG B (intentional): should be <= reorder_point
    low_stock_count = sum(1 for item in inventory if item["quantity"] < item["reorder_point"])
    pending_orders = sum(
        1 for order in orders if order["status"] in {"Processing", "Backordered"}
    )
    total_value = round(sum(item["quantity"] * item["unit_cost"] for item in inventory), 2)

    # BUG C (intentional): frontend expects totalValue
    return {
        "inventoryCount": len(inventory),
        "pendingOrders": pending_orders,
        "lowStockCount": low_stock_count,
        "total_value": total_value,
    }


@app.get("/api/risk/suppliers")
def get_supplier_risk(
    warehouse: str | None = Query(default=None),
    category: str | None = Query(default=None),
) -> JSONResponse:
    # FEATURE TODO: implement supplier lead-time risk aggregation.
    return JSONResponse(status_code=501, content={"detail": "Not implemented yet"})


@app.get("/api/orders/export.csv", response_model=None)
def export_orders_csv(
    warehouse: str | None = Query(default=None),
    category: str | None = Query(default=None),
    order_status: str | None = Query(default=None),
    month: str | None = Query(default=None),
) -> JSONResponse | PlainTextResponse:
    # FEATURE TODO: implement CSV export that honors filters.
    _ = (warehouse, category, order_status, month)
    return JSONResponse(status_code=501, content={"detail": "Not implemented yet"})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
