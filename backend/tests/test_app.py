import asyncio

import pytest
from fastapi.testclient import TestClient
from main import app
from models.schemas import AlertCreate
from services.alert_service import AlertService, alert_service
from services.price_generator import PriceGenerator
from services.websocket_manager import WebSocketManager


@pytest.fixture
def client():
    alert_service._alerts.clear()
    with TestClient(app) as client:
        yield client
    alert_service._alerts.clear()


def test_health_stocks_and_alert_lifecycle(client):
    assert client.get('/').status_code == 200
    stocks = client.get('/stocks').json()
    assert {s['symbol'] for s in stocks} == {'AAPL', 'MSFT', 'TSLA', 'NVDA'}
    assert all(s['price'] > 0 for s in stocks)
    response = client.post('/alerts', json={'symbol': 'aapl', 'condition': 'above', 'target_price': 1})
    assert response.status_code == 201
    assert response.json()['symbol'] == 'AAPL'
    assert client.get('/alerts').json()[0]['id'] == response.json()['id']


@pytest.mark.parametrize('payload', [
    {'symbol': 'UNKNOWN', 'condition': 'above', 'target_price': 100},
    {'symbol': '', 'condition': 'above', 'target_price': 100},
    {'symbol': 'AAPL', 'condition': 'other', 'target_price': 100},
    {'symbol': 'AAPL', 'condition': 'above', 'target_price': 0},
    {'symbol': 'AAPL', 'condition': 'above', 'target_price': -1},
    {'symbol': 'AAPL', 'condition': 'above', 'target_price': 'Infinity'},
])
def test_invalid_alerts_are_rejected_without_storage(client, payload):
    assert client.post('/alerts', json=payload).status_code == 422
    assert client.get('/alerts').json() == []


@pytest.mark.parametrize('condition', ['above', 'below'])
def test_alert_fires_once_at_inclusive_boundary(condition):
    generator = PriceGenerator({'AAPL': 100})
    service = AlertService()
    alert = service.create_alert(AlertCreate(symbol='AAPL', condition=condition, target_price=100))
    assert [a.id for a in service.check_alerts(generator.snapshot())] == [alert.id]
    assert service.check_alerts(generator.snapshot()) == []
    assert service.get_alerts()[0].triggered_at is not None


def test_snapshot_does_not_advance_and_tick_remains_positive():
    generator = PriceGenerator({'AAPL': .01})
    assert generator.snapshot()['AAPL'].price == .01
    for _ in range(100):
        assert generator.tick()['AAPL'].price >= .01


def test_websocket_snapshot_tick_and_alert_delivery(client):
    alert = client.post('/alerts', json={'symbol': 'AAPL', 'condition': 'above', 'target_price': 1}).json()
    with client.websocket_connect('/ws/prices') as ws:
        initial = ws.receive_json()
        assert initial['type'] == 'price_update'
        assert len(initial['stocks']) == 4
        tick = ws.receive_json()
        assert [a['id'] for a in tick['triggered_alerts']] == [alert['id']]
        assert tick['stocks'][0]['updated_at'] != initial['stocks'][0]['updated_at']
        assert client.get('/alerts').json()[0]['triggered'] is True


def test_broadcast_removes_failed_client_and_keeps_healthy_client():
    class Client:
        def __init__(self, fails):
            self.fails = fails
            self.messages = []
        async def send_text(self, message):
            if self.fails:
                raise RuntimeError('closed')
            self.messages.append(message)
    manager = WebSocketManager()
    stale, healthy = Client(True), Client(False)
    manager.active_connections = [stale, healthy]
    asyncio.run(manager.broadcast({'type': 'price_update'}))
    assert manager.active_connections == [healthy]
    assert len(healthy.messages) == 1


def test_cors_allows_configured_local_frontend(client):
    response = client.options('/alerts', headers={
        'Origin': 'http://localhost:5173', 'Access-Control-Request-Method': 'POST'})
    assert response.status_code == 200
    assert response.headers['access-control-allow-origin'] == 'http://localhost:5173'
