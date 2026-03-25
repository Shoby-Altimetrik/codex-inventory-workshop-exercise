def test_feature_supplier_risk_endpoint_returns_risk_rows(client):
    response = client.get('/api/risk/suppliers')
    assert response.status_code == 200
    rows = response.json()
    assert isinstance(rows, list)
    assert rows
    required = {'supplier', 'avg_lead_time_days', 'risk_level', 'affected_skus'}
    assert required.issubset(rows[0].keys())


def test_feature_orders_csv_export_returns_csv(client):
    response = client.get('/api/orders/export.csv?warehouse=Dallas')
    assert response.status_code == 200
    assert response.headers['content-type'].startswith('text/csv')
    assert 'order_id' in response.text
