# backend/tests/conftest.py
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest.fixture
def client_factory():
    def _build(router):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)
    return _build