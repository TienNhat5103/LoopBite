# tests/test_order_router.py
from types import SimpleNamespace
from unittest.mock import MagicMock

import importlib

order_router = importlib.import_module("routers.order_router")


def test_get_all_orders(client_factory, monkeypatch):
    client = client_factory(order_router.router)
    fake = MagicMock()

    table = MagicMock()
    table.select.return_value = table
    table.execute.return_value = SimpleNamespace(data=[{"id": 1, "user_id": "u-1", "amount": 50.0}])
    fake.table.return_value = table
    monkeypatch.setattr(order_router, "supabase", fake)

    res = client.get("/api/v1/orders/")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_order_by_id_not_found(client_factory, monkeypatch):
    client = client_factory(order_router.router)
    fake = MagicMock()
    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(data=[])
    fake.table.return_value = table
    monkeypatch.setattr(order_router, "supabase", fake)

    res = client.get("/api/v1/orders/999")
    assert res.status_code == 404

def test_create_order_success(client_factory, monkeypatch):
    client = client_factory(order_router.router)
    fake = MagicMock()

    fake.auth.get_user.return_value = SimpleNamespace(user=SimpleNamespace(id="u-1"))

    food_table = MagicMock()
    food_table.select.return_value = food_table
    food_table.eq.return_value = food_table
    food_table.execute.return_value = SimpleNamespace(data=[{"price": 10.0, "name": "Pho", "quantity": 10}])

    orders_table = MagicMock()
    orders_table.insert.return_value = orders_table
    orders_table.execute.return_value = SimpleNamespace(data=[{"id": 100}])

    order_items_table = MagicMock()
    order_items_table.insert.return_value = order_items_table
    order_items_table.execute.return_value = SimpleNamespace(data=[{"id": 1}])

    food_update_table = MagicMock()
    food_update_table.update.return_value = food_update_table
    food_update_table.eq.return_value = food_update_table
    food_update_table.execute.return_value = SimpleNamespace(data=[{"id": 1}])

    def table_router(name):
        if name == "food":
            # first call for stock check, later call for stock update
            return food_table if not hasattr(table_router, "called") else food_update_table
        if name == "orders":
            return orders_table
        if name == "order_items":
            return order_items_table
        return MagicMock()
    table_router.called = False

    def table_side_effect(name):
        if name == "food" and not table_router.called:
            table_router.called = True
            return food_table
        if name == "food":
            return food_update_table
        if name == "orders":
            return orders_table
        if name == "order_items":
            return order_items_table
        return MagicMock()

    fake.table.side_effect = table_side_effect
    monkeypatch.setattr(order_router, "supabase", fake)

    payload = {"purchase_type": "delivery", "items": [{"food_id": 1, "quantity": 2}]}
    res = client.post("/api/v1/orders/", json=payload, headers={"Authorization": "Bearer token-1"})
    assert res.status_code == 201
    assert res.json()["order_id"] == 100

def test_delete_order(client_factory, monkeypatch):
    client = client_factory(order_router.router)
    fake = MagicMock()
    table = MagicMock()
    table.delete.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(data=[])
    fake.table.return_value = table
    monkeypatch.setattr(order_router, "supabase", fake)

    res = client.delete("/api/v1/orders/1")
    assert res.status_code == 200

def test_update_order_status_success(client_factory, monkeypatch):
    client = client_factory(order_router.router)
    fake = MagicMock()

    check_table = MagicMock()
    check_table.select.return_value = check_table
    check_table.eq.return_value = check_table
    check_table.execute.side_effect = [
        SimpleNamespace(data=[{"id": 1}]),  # check exists
        SimpleNamespace(data=[{"id": 1, "status": "confirmed"}]),  # update return
    ]
    check_table.update.return_value = check_table
    fake.table.return_value = check_table

    monkeypatch.setattr(order_router, "supabase", fake)
    res = client.put("/api/v1/orders/1/status", json={"status": "confirmed"})
    assert res.status_code == 200
    assert res.json()["success"] is True