# tests/test_profile_router.py
from types import SimpleNamespace
from unittest.mock import MagicMock

import importlib

profile_router = importlib.import_module("routers.profile_router")


def test_get_all_profiles(client_factory, monkeypatch):
    client = client_factory(profile_router.router)
    fake = MagicMock()

    table = MagicMock()
    table.select.return_value = table
    table.execute.return_value = SimpleNamespace(data=[{"id": "u-1", "role": "customer"}])
    fake.table.return_value = table

    monkeypatch.setattr(profile_router, "supabase", fake)
    res = client.get("/api/v1/profiles/")
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_update_profile_success(client_factory, monkeypatch):
    client = client_factory(profile_router.router)
    fake = MagicMock()

    table = MagicMock()
    table.update.return_value = table
    table.eq.return_value = table
    table.execute.return_value = SimpleNamespace(data=[{"id": "u-1", "full_name": "Alice", "role": "merchant"}])
    fake.table.return_value = table

    monkeypatch.setattr(profile_router, "supabase", fake)
    res = client.put("/api/v1/profiles/u-1", json={"full_name": "Alice", "role": "merchant"})
    assert res.status_code == 200
    assert res.json()["role"] == "merchant"

def test_update_profile_empty_payload(client_factory):
    client = client_factory(profile_router.router)
    res = client.put("/api/v1/profiles/u-1", json={})
    assert res.status_code == 400