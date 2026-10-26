from __future__ import annotations

import httpx
import pytest
from bank_api.api import app
from bank_api.async_client import AsyncAccountAggregator
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


@pytest.mark.anyio
async def test_api_root() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200


def test_create_client_and_account(client: TestClient) -> None:
    c_res = client.post("/clients", json={"full_name": "Anna Koval", "email": "anna@bank.ua"})
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

    a_res = client.post(
        "/accounts", json={"account_number": "UA-ST-1", "client_id": c_id, "initial_balance": 100.0}
    )
    assert a_res.status_code == 201
    assert a_res.json()["account_number"] == "UA-ST-1"


def test_invalid_data(client: TestClient) -> None:
    # Invalid email or missing required fields triggers 422
    response = client.post("/clients", json={"full_name": 12345})
    assert response.status_code == 422


def test_delete_account(client: TestClient) -> None:
    c_res = client.post("/clients", json={"full_name": "Delete User", "email": "del@bank.ua"})
    c_id = c_res.json()["id"]
    a_res = client.post(
        "/accounts", json={"account_number": "UA-DEL-1", "client_id": c_id, "initial_balance": 50.0}
    )
    acc_id = a_res.json()["id"]

    del_res = client.delete(f"/accounts/{acc_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/accounts/{acc_id}")
    assert get_res.status_code == 404


def test_pagination_and_filtering(client: TestClient) -> None:
    c_res = client.post("/clients", json={"full_name": "Filter User", "email": "filter@bank.ua"})
    c_id = c_res.json()["id"]

    client.post(
        "/accounts", json={"account_number": "UA-PAG-1", "client_id": c_id, "initial_balance": 10.0}
    )
    client.post(
        "/accounts", json={"account_number": "UA-PAG-2", "client_id": c_id, "initial_balance": 20.0}
    )

    p_res = client.get(f"/accounts?client_id={c_id}&limit=1&offset=0")
    assert p_res.status_code == 200
    assert len(p_res.json()) == 1


def test_banking_api_lifecycle(client: TestClient) -> None:
    c_res = client.post(
        "/clients", json={"full_name": "Artem Kyrychenko", "email": "zoom.2000v@gmail.com"}
    )
    assert c_res.status_code == 201
    c_id = c_res.json()["id"]

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

    dep_res = client.post(f"/accounts/{a1_id}/deposit", json={"amount": 500.0})
    assert dep_res.status_code == 200
    assert dep_res.json()["balance"] == 1500.0

    w_res = client.post(f"/accounts/{a1_id}/withdraw", json={"amount": 300.0})
    assert w_res.status_code == 200
    assert w_res.json()["balance"] == 1200.0

    tx_res = client.post(
        "/transfers", json={"source_account_id": a1_id, "target_account_id": a2_id, "amount": 400.0}
    )
    assert tx_res.status_code == 200
    assert tx_res.json()["source_balance"] == 800.0
    assert tx_res.json()["target_balance"] == 600.0

    txs_res = client.get(f"/accounts/{a1_id}/transactions")
    assert txs_res.status_code == 200
    assert len(txs_res.json()) >= 3

    tf_res = client.get("/total-funds")
    assert tf_res.status_code == 200
    assert tf_res.json()["total_funds"] == 1400.0

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
