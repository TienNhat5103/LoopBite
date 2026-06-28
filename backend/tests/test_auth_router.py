# tests/test_auth_router.py
from types import SimpleNamespace
from unittest.mock import MagicMock
import importlib
auth_router = importlib.import_module("routers.auth_router")

def test_register_user_success(client_factory, monkeypatch):
    client = client_factory(auth_router.router)
    fake_supabase = MagicMock()
    fake_supabase.auth.sign_up.return_value = SimpleNamespace(
        user=SimpleNamespace(id="u-1")
    )
    monkeypatch.setattr(auth_router, "supabase", fake_supabase)

    payload = {"email": "a@b.com", "password": "123456", "full_name": "Alice"}
    res = client.post("/api/v1/auth/register", json=payload)

    assert res.status_code == 201
    assert res.json()["user_id"] == "u-1"

def test_login_user_success(client_factory, monkeypatch):
    client = client_factory(auth_router.router)
    fake_supabase = MagicMock()
    fake_supabase.auth.sign_in_with_password.return_value = SimpleNamespace(
        session=SimpleNamespace(access_token="token-123"),
        user=SimpleNamespace(id="u-1", email="a@b.com"),
    )
    monkeypatch.setattr(auth_router, "supabase", fake_supabase)

    res = client.post("/api/v1/auth/login", json={"email": "a@b.com", "password": "123456"})
    assert res.status_code == 200
    body = res.json()
    assert body["access_token"] == "token-123"
    assert body["token_type"] == "bearer"
    assert body["user"]["id"] == "u-1"

def test_get_me_success(client_factory, monkeypatch):
    client = client_factory(auth_router.router)
    fake_supabase = MagicMock()

    fake_supabase.auth.get_user.return_value = SimpleNamespace(user=SimpleNamespace(id="u-1"))

    table = MagicMock()
    table.select.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(
        data=[{"id": "u-1", "full_name": "Alice", "role": "customer"}]
    )
    fake_supabase.table.return_value = table

    monkeypatch.setattr(auth_router, "supabase", fake_supabase)

    res = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer token-123"})
    assert res.status_code == 200
    assert res.json()["auth_id"] == "u-1"

def test_delete_user_success(client_factory, monkeypatch):
    client = client_factory(auth_router.router)
    fake_supabase = MagicMock()
    monkeypatch.setattr(auth_router, "supabase", fake_supabase)

    res = client.delete("/api/v1/auth/delete-user/u-1")
    assert res.status_code == 200
    assert "Thành công" in res.json()["status"]