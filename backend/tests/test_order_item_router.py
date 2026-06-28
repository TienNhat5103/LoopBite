# tests/test_order_item_router.py
from types import SimpleNamespace
from unittest.mock import MagicMock

import importlib

order_item_router = importlib.import_module("routers.order_item_router")


def test_get_all_order_items(client_factory, monkeypatch):
    client = client_factory(order_item_router.router)
    fake = MagicMock()
    table = MagicMock()
    table.select.return_value = table
    table.execute.return_value = SimpleNamespace(data=[{"id": 1, "order_id": 1, "food_id": 2, "quantity": 1, "total_price": 10.0}])
    fake.table.return_value = table
    monkeypatch.setattr(order_item_router, "supabase", fake)

    res = client.get("/api/v1/order-items/")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_create_order_item(client_factory, monkeypatch):
    client = client_factory(order_item_router.router)
    fake = MagicMock()
    table = MagicMock()
    table.insert.return_value = table
    table.execute.return_value = SimpleNamespace(data=[{"id": 2, "order_id": 1, "food_id": 3, "quantity": 2, "total_price": 20.0}])
    fake.table.return_value = table
    monkeypatch.setattr(order_item_router, "supabase", fake)

    payload = {"order_id": 1, "food_id": 3, "quantity": 2, "total_price": 20.0}
    res = client.post("/api/v1/order-items/", json=payload)
    assert res.status_code == 201

def test_delete_order_item(client_factory, monkeypatch):
    client = client_factory(order_item_router.router)
    fake = MagicMock()
    table = MagicMock()
    table.delete.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(data=[])
    fake.table.return_value = table
    monkeypatch.setattr(order_item_router, "supabase", fake)

    res = client.delete("/api/v1/order-items/2")
    assert res.status_code == 200