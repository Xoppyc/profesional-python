from __future__ import annotations

import pytest
from bank_api.api import accounts_db, app, clients_db, transactions_db
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> TestClient:
    clients_db.clear()
    accounts_db.clear()
    transactions_db.clear()
    return TestClient(app)
