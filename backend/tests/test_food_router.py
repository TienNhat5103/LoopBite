# tests/test_food_router.py
from types import SimpleNamespace
from unittest.mock import MagicMock
import importlib
food_router = importlib.import_module("routers.food_router")


def test_get_all_food_success(client_factory, monkeypatch):
    client = client_factory(food_router.router)
    fake_supabase = MagicMock()

    table = MagicMock()
    table.select.return_value = table
    table.order.return_value = table
    table.execute.return_value = SimpleNamespace(
        data=[{"id": 1, "merchant_id": 2, "name": "Banh", "price": 10.0, "quantity": 5, "status": "active"}]
    )
    fake_supabase.table.return_value = table
    monkeypatch.setattr(food_router, "supabase", fake_supabase)

    res = client.get("/api/v1/food/")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_food_by_id_not_found(client_factory, monkeypatch):
    client = client_factory(food_router.router)
    fake_supabase = MagicMock()

    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(data=[])
    fake_supabase.table.return_value = table
    monkeypatch.setattr(food_router, "supabase", fake_supabase)

    res = client.get("/api/v1/food/999")
    assert res.status_code == 404

def test_create_food_success(client_factory, monkeypatch):
    client = client_factory(food_router.router)
    fake_supabase = MagicMock()

    table = MagicMock()
    table.insert.return_value = table
    table.execute.return_value = SimpleNamespace(
        data=[{"id": 11, "merchant_id": 2, "name": "Pho", "price": 30.0, "quantity": 8, "status": "active"}]
    )
    fake_supabase.table.return_value = table
    monkeypatch.setattr(food_router, "supabase", fake_supabase)

    payload = {"merchant_id": 2, "name": "Pho", "price": 30.0, "quantity": 8, "status": "active"}
    res = client.post("/api/v1/food/", json=payload)
    assert res.status_code == 201
    assert res.json()["id"] == 11

def test_update_food_success(client_factory, monkeypatch):
    client = client_factory(food_router.router)
    fake_supabase = MagicMock()

    # bypass auth dependency
    client.app.dependency_overrides[food_router.verify_merchant_role] = lambda: "merchant-1"

    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.update.return_value = table
    table.execute.side_effect = [
        SimpleNamespace(data=[{"id": 11}]),  # check exist
        SimpleNamespace(data=[{"id": 11, "merchant_id": 2, "name": "Pho", "price": 25.0, "quantity": 4, "status": "active"}]),
    ]
    table.select.return_value = table
    fake_supabase.table.return_value = table
    monkeypatch.setattr(food_router, "supabase", fake_supabase)

    res = client.put("/api/v1/food/11", json={"price": 25.0, "quantity": 4})
    assert res.status_code == 200
    assert res.json()["price"] == 25.0

def test_delete_food_success(client_factory, monkeypatch):
    client = client_factory(food_router.router)
    fake_supabase = MagicMock()

    client.app.dependency_overrides[food_router.verify_merchant_role] = lambda: "merchant-1"

    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.delete.return_value = table
    table.execute.side_effect = [
        SimpleNamespace(data=[{"id": 11}]),  # check exist
        SimpleNamespace(data=[]),            # delete
    ]
    fake_supabase.table.return_value = table
    monkeypatch.setattr(food_router, "supabase", fake_supabase)

    res = client.delete("/api/v1/food/11")
    assert res.status_code == 200