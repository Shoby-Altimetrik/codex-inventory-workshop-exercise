import { describe, expect, it, vi, beforeEach, afterEach } from 'vitest'
import { fetchOrders, fetchSupplierRisk } from '../api'

describe('API contract tests', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('uses order_status query key when filtering orders', async () => {
    fetch.mockResolvedValue({ json: async () => [] })

    await fetchOrders({
      warehouse: 'all',
      category: 'all',
      order_status: 'Processing',
      month: 'all'
    })

    const calledUrl = fetch.mock.calls[0][0]
    expect(calledUrl).toContain('order_status=Processing')
  })

  it('returns supplier risk rows as an array payload', async () => {
    fetch.mockResolvedValue({
      status: 501,
      json: async () => ({ detail: 'Not implemented yet' })
    })

    const data = await fetchSupplierRisk({ warehouse: 'all', category: 'all' })
    expect(Array.isArray(data)).toBe(true)
  })
})
