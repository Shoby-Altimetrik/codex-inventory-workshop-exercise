<script setup>
import { onMounted, ref } from 'vue'
import {
  fetchDashboardSummary,
  fetchOrders,
  fetchSupplierRisk,
  exportOrdersCsv
} from './api'

const filters = ref({
  warehouse: 'all',
  category: 'all',
  order_status: 'all',
  month: 'all'
})

const summary = ref({
  inventoryCount: 0,
  pendingOrders: 0,
  lowStockCount: 0,
  totalValue: 0
})

const orders = ref([])
const supplierRisk = ref([])
const riskError = ref('')

async function loadData() {
  summary.value = await fetchDashboardSummary(filters.value)
  orders.value = await fetchOrders(filters.value)

  const risk = await fetchSupplierRisk(filters.value)
  if (Array.isArray(risk)) {
    supplierRisk.value = risk
    riskError.value = ''
  } else {
    riskError.value = 'Supplier risk feature is pending implementation.'
  }
}

function onApplyFilters() {
  loadData()
}

function onExportCsv() {
  // FEATURE TODO (intentional): wire response blob to browser download flow.
  // Not calling exportOrdersCsv right now by design for workshop task.
  console.log('Export TODO')
}

onMounted(loadData)
</script>

<template>
  <main class="page">
    <header>
      <h1>Codex Inventory Workshop</h1>
      <p>Fix seeded issues and ship missing features with Codex.</p>
    </header>

    <section class="filters">
      <label>
        Warehouse
        <select v-model="filters.warehouse">
          <option value="all">All</option>
          <option value="Dallas">Dallas</option>
          <option value="Austin">Austin</option>
          <option value="Houston">Houston</option>
        </select>
      </label>

      <label>
        Category
        <select v-model="filters.category">
          <option value="all">All</option>
          <option value="Electronics">Electronics</option>
          <option value="Sensors">Sensors</option>
          <option value="Mechanical">Mechanical</option>
          <option value="Power">Power</option>
        </select>
      </label>

      <label>
        Order Status
        <select v-model="filters.order_status">
          <option value="all">All</option>
          <option value="Delivered">Delivered</option>
          <option value="Shipped">Shipped</option>
          <option value="Processing">Processing</option>
          <option value="Backordered">Backordered</option>
        </select>
      </label>

      <button @click="onApplyFilters">Apply</button>
      <button @click="onExportCsv">Export CSV</button>
    </section>

    <section class="cards">
      <article>
        <h2>Inventory Items</h2>
        <p data-testid="metric-inventory">{{ summary.inventoryCount }}</p>
      </article>
      <article>
        <h2>Pending Orders</h2>
        <p data-testid="metric-pending">{{ summary.pendingOrders }}</p>
      </article>
      <article>
        <h2>Low Stock Items</h2>
        <p data-testid="metric-low-stock">{{ summary.lowStockCount }}</p>
      </article>
      <article>
        <h2>Total Inventory Value</h2>
        <p data-testid="metric-total-value">{{ summary.totalValue }}</p>
      </article>
    </section>

    <section>
      <h2>Supplier Lead Time Risk</h2>
      <p v-if="riskError" class="warning">{{ riskError }}</p>
      <table v-if="supplierRisk.length > 0" data-testid="risk-table">
        <thead>
          <tr>
            <th>Supplier</th>
            <th>Avg Lead Time (Days)</th>
            <th>Risk Level</th>
            <th>Affected SKUs</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in supplierRisk" :key="row.supplier">
            <td>{{ row.supplier }}</td>
            <td>{{ row.avg_lead_time_days }}</td>
            <td>{{ row.risk_level }}</td>
            <td>{{ row.affected_skus.join(', ') }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2>Orders</h2>
      <ul>
        <li v-for="order in orders" :key="order.id">
          {{ order.id }} | {{ order.status }} | {{ order.warehouse }} | {{ order.total_value }}
        </li>
      </ul>
    </section>
  </main>
</template>

<style scoped>
.page {
  margin: 0 auto;
  max-width: 980px;
  padding: 24px;
  font-family: "Avenir Next", "Segoe UI", sans-serif;
  color: #0f172a;
}

.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: end;
  margin: 20px 0;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 10px;
  margin-bottom: 20px;
}

article {
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 12px;
  background: #f8fafc;
}

.warning {
  color: #9a3412;
  font-weight: 600;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th,
td {
  border: 1px solid #e2e8f0;
  padding: 8px;
  text-align: left;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  border-bottom: 1px solid #e2e8f0;
  padding: 6px 0;
}
</style>
