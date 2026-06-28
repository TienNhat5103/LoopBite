# tests/test_search_engines.py
from unittest.mock import MagicMock

import importlib

search_engines = importlib.import_module("routers.search_engines")


def test_normalize_text():
    assert search_engines.normalize_text("Bánh mì Đặc biệt") == "banh mi dac biet"

def test_haversine_km_same_point():
    d = search_engines.haversine_km(10.0, 106.0, 10.0, 106.0)
    assert round(d, 5) == 0

def test_search_foods_endpoint_success(client_factory, monkeypatch):
    client = client_factory(search_engines.router)

    fake_service = MagicMock()
    fake_service.search_food_nearby.return_value = [
        {
            "merchant": {"id": 1, "name": "FM", "distance_km": 0.25},
            "foods": [{"id": 2, "name": "Banh Mi", "merchant_id": 1}],
        }
    ]
    monkeypatch.setattr(search_engines, "search_service", fake_service)

    res = client.get("/api/v1/search/foods", params={"keyword": "banh", "user_lat": 10.0, "user_lng": 106.0})
    assert res.status_code == 200
    body = res.json()
    assert body["keyword"] == "banh"
    assert len(body["results"]) == 1