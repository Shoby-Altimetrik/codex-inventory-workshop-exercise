const API_BASE = 'http://localhost:8001'

function buildQuery(params) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value && value !== 'all') {
      query.set(key, value)
    }
  })
  return query.toString()
}

export async function fetchDashboardSummary(filters) {
  const query = buildQuery(filters)
  const response = await fetch(`${API_BASE}/api/dashboard/summary?${query}`)
  return response.json()
}

export async function fetchOrders(filters) {
  // BUG A (intentional): backend expects `order_status`, not `status`
  const query = buildQuery({
    warehouse: filters.warehouse,
    category: filters.category,
    status: filters.order_status,
    month: filters.month
  })

  const response = await fetch(`${API_BASE}/api/orders?${query}`)
  return response.json()
}

export async function fetchSupplierRisk(filters) {
  const query = buildQuery(filters)
  const response = await fetch(`${API_BASE}/api/risk/suppliers?${query}`)
  return response.json()
}

export async function exportOrdersCsv(filters) {
  const query = buildQuery(filters)
  return fetch(`${API_BASE}/api/orders/export.csv?${query}`)
}
