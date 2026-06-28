# 🚀 Ensuring Web Application Reliability via Robust Integration Testing

To guarantee that our web application runs successfully, remains stable under production-like conditions, and prevents regressions, we implemented a comprehensive **automated testing suite** using **Pytest** and **FastAPI TestClient**.

By isolating routers, mocking third-party dependencies (such as Supabase), and leveraging reusable fixtures, the test suite provides high code coverage and predictable behavior across all API layers.

---

# 🛠️ 1. Core Testing Architecture

The testing framework decouples the database layer from the HTTP endpoints, allowing tests to execute quickly without modifying production or staging data.

## 🧱 Architecture Overview

- **Decoupled Routers**
  - Each router is mounted independently inside a clean `FastAPI` instance.

- **Strict Mocking**
  - External services such as `Supabase` and geolocation utilities are replaced with `unittest.mock.MagicMock`.

- **Fixture-Driven Design**
  - Shared client initialization logic is encapsulated within reusable Pytest fixtures.

---

# ⚙️ 2. Test Configuration & Reusable Fixtures

The testing utilities are centralized in `conftest.py`, which configures the Python runtime path and provides a factory fixture for generating isolated test clients.

```python
# backend/tests/conftest.py

import sys
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Resolve backend directory
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture
def client_factory():
    """
    Factory fixture for creating isolated FastAPI
    applications with the target router.
    """

    def _build(router):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    return _build
```

---

# 🧪 3. Test Coverage

The test suite covers every major functional component of the application.

## 🔹 Authentication & Security (`test_auth_router.py`)

Validates user authentication, payload schemas, and session management.

### Covered Tests

- `test_register_user_success`
  - Confirms successful user registration.

- `test_login_user_success`
  - Validates JWT Bearer token generation.

- `test_get_me_success`
  - Verifies authenticated user information retrieval.

---

## 🔹 Merchant & Storefront (`test_merchant_router.py`)

Ensures merchant management APIs behave correctly.

### Covered Scenarios

- Merchant list pagination (`GET /api/v1/merchants/`)
- Merchant food lookup (`GET /merchant_food/{id}`)
- Invalid merchant handling (`404 Not Found`)

---

## 🔹 Order & Inventory Management (`test_order_router.py`)

Tests complex ordering workflows involving multiple database tables.

### Example Mocking Strategy

```python
def table_side_effect(name):
    if name == "food" and not table_router.called:
        table_router.called = True
        return food_table          # Stock lookup

    if name == "food":
        return food_update_table   # Inventory update

    ...
```

This approach allows multiple mocked database tables to be returned during different stages of the order lifecycle.

---

## 🔹 Search & Geolocation (`test_search_engines.py`)

Validates utility functions without requiring external search services.

### Covered Tests

- `test_normalize_text`
  - Verifies text normalization.

  Example:

  ```
  "Bánh mì Đặc biệt"
      ↓
  "banh mi dac biet"
  ```

- `test_haversine_km_same_point`
  - Validates the correctness of the Haversine distance calculation.

---

# 📊 4. Endpoint Coverage

| Endpoint | Method | Expected Status | Purpose |
|----------|--------|-----------------|---------|
| `/api/v1/auth/register` | `POST` | **201 Created** | Register a new user |
| `/api/v1/auth/login` | `POST` | **200 OK** | Authenticate user and return JWT |
| `/api/v1/merchants/` | `GET` | **200 OK** | Retrieve merchant list |
| `/api/v1/merchants/{id}` | `GET` | **404 Not Found** | Handle invalid merchant IDs |
| `/api/v1/food/{id}` | `PUT` | **200 OK** | Update food inventory |
| `/api/v1/orders/` | `POST` | **201 Created** | Create an order and deduct stock |
| `/api/v1/profiles/{id}` | `PUT` | **400 Bad Request** | Reject invalid update requests |

---

# 🚀 5. Running the Test Suite

Run the complete test suite:

```bash
pytest -q
```


# ✅ Summary

The automated testing framework ensures that:

- API endpoints behave consistently.
- Authentication and authorization remain secure.
- Database interactions are correctly mocked.
- Inventory and order workflows operate reliably.
- Search and geolocation utilities produce accurate results.
- Future code changes do not introduce regressions.

By integrating these tests into the CI/CD pipeline, every code change is automatically validated before deployment, helping maintain a stable and reliable production environment.

