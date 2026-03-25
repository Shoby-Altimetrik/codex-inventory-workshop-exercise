import { describe, expect, it, vi } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import App from '../App.vue'

vi.mock('../api', () => {
  return {
    fetchDashboardSummary: vi.fn(async () => ({
      inventoryCount: 4,
      pendingOrders: 2,
      lowStockCount: 3,
      totalValue: 5047
    })),
    fetchOrders: vi.fn(async () => []),
    fetchSupplierRisk: vi.fn(async () => [
      {
        supplier: 'GridLite Power',
        avg_lead_time_days: 33,
        risk_level: 'high',
        affected_skus: ['PWR-404']
      }
    ]),
    exportOrdersCsv: vi.fn(async () => ({ ok: true }))
  }
})

import { exportOrdersCsv } from '../api'

describe('App feature tests', () => {
  it('renders supplier risk table when rows exist', async () => {
    const wrapper = mount(App)
    await flushPromises()
    expect(wrapper.find('[data-testid="risk-table"]').exists()).toBe(true)
  })

  it('clicking Export CSV triggers exportOrdersCsv', async () => {
    const wrapper = mount(App)
    await flushPromises()
    await wrapper.find('button:last-of-type').trigger('click')
    expect(exportOrdersCsv).toHaveBeenCalled()
  })
})
