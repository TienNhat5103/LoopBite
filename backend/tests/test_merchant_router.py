from types import SimpleNamespace
from unittest.mock import MagicMock
import importlib

merchant_router = importlib.import_module("routers.merchant_router")


def _mock_table(data):
    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.order.return_value = table
    table.insert.return_value = table
    table.update.return_value = table
    table.delete.return_value = table
    table.execute.return_value = SimpleNamespace(data=data)
    return table


def test_get_all_merchants(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()
    fake.table.return_value = _mock_table([{"id": 1, "name": "FM"}])
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.get("/api/v1/merchants/")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_merchant_by_id_not_found(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()
    fake.table.return_value = _mock_table([])
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.get("/api/v1/merchants/999")
    assert res.status_code == 404


def test_get_food_by_merchant_success(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()

    # Must satisfy response_model=List[Food]
    fake.table.return_value = _mock_table(
        [
            {
                "id": 1,
                "merchant_id": 2,
                "name": "Pho",
                "category": "noodle",
                "price": 35000.0,
                "quantity": 10,
                "status": "active",
            }
        ]
    )
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.get("/api/v1/merchants/merchant_food/2")
    assert res.status_code == 200
    body = res.json()
    assert body[0]["merchant_id"] == 2
    assert body[0]["price"] == 35000.0
    assert body[0]["quantity"] == 10
    assert body[0]["status"] == "active"


def test_create_merchant(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()
    fake.table.return_value = _mock_table([{"id": 10, "name": "Shop"}])
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.post("/api/v1/merchants/", json={"name": "Shop"})
    assert res.status_code == 201
    assert res.json()["id"] == 10


def test_update_merchant(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()
    fake.table.return_value = _mock_table([{"id": 10, "name": "New Name"}])
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.put("/api/v1/merchants/10", json={"name": "New Name"})
    assert res.status_code == 200
    assert res.json()["name"] == "New Name"


def test_delete_merchant(client_factory, monkeypatch):
    client = client_factory(merchant_router.router)
    fake = MagicMock()
    fake.table.return_value = _mock_table([])
    monkeypatch.setattr(merchant_router, "supabase", fake)

    res = client.delete("/api/v1/merchants/10")
    assert res.status_code == 200
    assert "Đã xóa cửa hàng" in res.json()["message"]