from fastapi.testclient import TestClient
from bank_api.api import app, accounts_db, clients_db, transactions_db

client = TestClient(app)


def setup_function() -> None:
    clients_db.clear()
    accounts_db.clear()
    transactions_db.clear()


def test_health_check() -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_banking_api_lifecycle() -> None:
    # 1. Create Client
    c_res = client.post("/clients", json={"full_name": "Artem Kyrychenko", "email": "zoom.2000v@gmail.com"})
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

    # 2. Create Two Accounts
    a1_res = client.post("/accounts", json={"account_number": "UA801", "client_id": c_id, "initial_balance": 1000.0})
    a2_res = client.post("/accounts", json={"account_number": "UA802", "client_id": c_id, "initial_balance": 200.0})
    assert a1_res.status_code == 201
    assert a2_res.status_code == 201
    a1_id = a1_res.json()["id"]
    a2_id = a2_res.json()["id"]

    # 3. Deposit
    dep_res = client.post(f"/accounts/{a1_id}/deposit", json={"amount": 500.0})
    assert dep_res.status_code == 200
    assert dep_res.json()["balance"] == 1500.0

    # 4. Withdraw
    w_res = client.post(f"/accounts/{a1_id}/withdraw", json={"amount": 300.0})
    assert w_res.status_code == 200
    assert w_res.json()["balance"] == 1200.0

    # 5. Transfer
    tx_res = client.post("/transfers", json={"source_account_id": a1_id, "target_account_id": a2_id, "amount": 400.0})
    assert tx_res.status_code == 200
    assert tx_res.json()["source_balance"] == 800.0
    assert tx_res.json()["target_balance"] == 600.0

    # 6. Negative overdraft rejected
    fail_res = client.post("/transfers", json={"source_account_id": a1_id, "target_account_id": a2_id, "amount": 9999.0})
    assert fail_res.status_code == 400
