def test_bug_a_status_filter_param_should_work(client):
    # Workshop expectation: status filtering should work for status=Processing.
    # Current backend only honors order_status, so this fails initially.
    response = client.get('/api/orders?status=Processing')
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 1
    assert rows[0]['status'] == 'Processing'


def test_bug_b_low_stock_should_include_equal_reorder_point(client):
    response = client.get('/api/dashboard/summary')
    assert response.status_code == 200
    summary = response.json()
    # Current data includes an item with quantity == reorder_point (SNS-020).
    # Expecting it to be counted as low stock.
    assert summary['lowStockCount'] == 3


def test_bug_c_dashboard_should_return_camel_case_total_value(client):
    response = client.get('/api/dashboard/summary')
    assert response.status_code == 200
    summary = response.json()
    assert 'totalValue' in summary
