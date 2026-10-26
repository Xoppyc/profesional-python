from __future__ import annotations

import httpx
import pytest
from bank_api.async_client import AsyncAccountAggregator
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_banking_api_lifecycle(client: TestClient) -> None:
    # 1. Create Client
    c_res = client.post(
        "/clients", json={"full_name": "Artem Kyrychenko", "email": "zoom.2000v@gmail.com"}
    )
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

    # 2. Create Two Accounts
    a1_res = client.post(
        "/accounts", json={"account_number": "UA801", "client_id": c_id, "initial_balance": 1000.0}
    )
    a2_res = client.post(
        "/accounts", json={"account_number": "UA802", "client_id": c_id, "initial_balance": 200.0}
    )
    assert a1_res.status_code == 201
    assert a2_res.status_code == 201
    a1_id = a1_res.json()["id"]
    a2_id = a2_res.json()["id"]

    # 3. Get Account
    get_res = client.get(f"/accounts/{a1_id}")
    assert get_res.status_code == 200
    assert get_res.json()["account_number"] == "UA801"

    # 4. Deposit
    dep_res = client.post(f"/accounts/{a1_id}/deposit", json={"amount": 500.0})
    assert dep_res.status_code == 200
    assert dep_res.json()["balance"] == 1500.0

    # 5. Withdraw
    w_res = client.post(f"/accounts/{a1_id}/withdraw", json={"amount": 300.0})
    assert w_res.status_code == 200
    assert w_res.json()["balance"] == 1200.0

    # 6. Transfer
    tx_res = client.post(
        "/transfers", json={"source_account_id": a1_id, "target_account_id": a2_id, "amount": 400.0}
    )
    assert tx_res.status_code == 200
    assert tx_res.json()["source_balance"] == 800.0
    assert tx_res.json()["target_balance"] == 600.0

    # 7. Check transactions history
    txs_res = client.get(f"/accounts/{a1_id}/transactions")
    assert txs_res.status_code == 200
    assert len(txs_res.json()) >= 3

    # 8. Total funds
    tf_res = client.get("/total-funds")
    assert tf_res.status_code == 200
    assert tf_res.json()["total_funds"] == 1400.0

    # 9. Negative overdraft rejected
    fail_res = client.post(
        "/transfers",
        json={"source_account_id": a1_id, "target_account_id": a2_id, "amount": 9999.0},
    )
    assert fail_res.status_code == 400


@pytest.mark.anyio
async def test_async_account_aggregator() -> None:
    aggregator = AsyncAccountAggregator(base_url="http://testserver", max_concurrency=2)

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        url = str(request.url)
        if "accounts/1" in url:
            return httpx.Response(200, json={"id": 1, "account_number": "UA801", "balance": 800.0})
        if "accounts/2" in url:
            return httpx.Response(200, json={"id": 2, "account_number": "UA802", "balance": 600.0})
        return httpx.Response(404, json={"detail": "Not found"})

    transport = httpx.MockTransport(mock_handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as async_client:
        results = await aggregator.fetch_multiple_accounts(async_client, [1, 2, 99])
        assert len(results) == 2
        assert results[0]["id"] == 1
        assert results[1]["id"] == 2
