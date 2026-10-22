from collections.abc import Generator
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool
from bank_account_service.api import app
from bank_account_service.database import Base, get_db

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_production_health() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "bank-account-service"}


def test_full_account_lifecycle() -> None:
    # 1. Register Client
    c_res = client.post("/clients", json={"full_name": "Artem Kyrychenko", "email": "zoom.2000v@gmail.com"})
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

    # 2. Register Accounts
    a1 = client.post("/accounts", json={"account_number": "UA9001", "client_id": c_id, "initial_balance": 2000.0}).json()
    a2 = client.post("/accounts", json={"account_number": "UA9002", "client_id": c_id, "initial_balance": 500.0}).json()

    # 3. Transfer
    tx = client.post("/transfers", json={"source_account_id": a1["id"], "target_account_id": a2["id"], "amount": 750.0})
    assert tx.status_code == 200
    assert tx.json()["source_balance"] == 1250.0
    assert tx.json()["target_balance"] == 1250.0

    # 4. Check transactions
    history = client.get(f"/accounts/{a1['id']}/transactions").json()
    assert len(history) == 1
    assert history[0]["operation"] == "transfer_out"
