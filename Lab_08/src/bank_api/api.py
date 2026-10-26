from datetime import UTC, datetime

from fastapi import FastAPI, HTTPException, status

from bank_api.schemas import (
    AccountCreate,
    AccountResponse,
    AmountPayload,
    ClientCreate,
    ClientResponse,
    TransactionResponse,
    TransferPayload,
)

app = FastAPI(title="Bank Account REST API", version="0.8.0")

# In-memory storage for demonstration
clients_db: dict[int, dict] = {}
accounts_db: dict[int, dict] = {}
transactions_db: list[dict] = []
_id_seq = 1


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "bank-api"}


@app.get("/accounts", response_model=list[AccountResponse])
def list_accounts() -> list[dict]:
    return list(accounts_db.values())


@app.get("/total-funds")
def get_total_funds() -> dict[str, float]:
    total = sum(acc["balance"] for acc in accounts_db.values())
    return {"total_funds": round(total, 2)}


@app.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate) -> dict:
    global _id_seq
    client_id = _id_seq
    _id_seq += 1
    record = {"id": client_id, "full_name": payload.full_name, "email": payload.email}
    clients_db[client_id] = record
    return record


@app.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate) -> dict:
    global _id_seq
    if payload.client_id not in clients_db:
        raise HTTPException(status_code=404, detail="Referenced client does not exist")

    for acc in accounts_db.values():
        if acc["account_number"] == payload.account_number:
            raise HTTPException(status_code=400, detail="Account number already registered")

    acc_id = _id_seq
    _id_seq += 1
    account_record = {
        "id": acc_id,
        "account_number": payload.account_number,
        "client_id": payload.client_id,
        "balance": payload.initial_balance,
    }
    accounts_db[acc_id] = account_record
    return account_record


@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int) -> dict:
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@app.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_account_transactions(account_id: int) -> list[dict]:
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")
    return [tx for tx in transactions_db if tx["account_id"] == account_id]


@app.post("/accounts/{account_id}/deposit", response_model=AccountResponse)
def deposit(account_id: int, payload: AmountPayload) -> dict:
    global _id_seq
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account["balance"] += payload.amount
    tx = {
        "id": _id_seq,
        "account_id": account_id,
        "operation": "deposit",
        "amount": payload.amount,
        "created_at": datetime.now(UTC),
    }
    _id_seq += 1
    transactions_db.append(tx)
    return account


@app.post("/accounts/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(account_id: int, payload: AmountPayload) -> dict:
    global _id_seq
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if account["balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for withdrawal")

    account["balance"] -= payload.amount
    tx = {
        "id": _id_seq,
        "account_id": account_id,
        "operation": "withdraw",
        "amount": payload.amount,
        "created_at": datetime.now(UTC),
    }
    _id_seq += 1
    transactions_db.append(tx)
    return account


@app.post("/transfers", status_code=status.HTTP_200_OK)
def transfer(payload: TransferPayload) -> dict:
    global _id_seq
    source = accounts_db.get(payload.source_account_id)
    target = accounts_db.get(payload.target_account_id)

    if not source or not target:
        raise HTTPException(status_code=404, detail="Source or target account not found")

    if source["balance"] < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds on source account")

    # Atomic debit and credit with twin ledger transactions
    source["balance"] -= payload.amount
    target["balance"] += payload.amount

    now = datetime.now(UTC)
    tx_out = {
        "id": _id_seq,
        "account_id": source["id"],
        "operation": "transfer_out",
        "amount": payload.amount,
        "created_at": now,
    }
    _id_seq += 1
    tx_in = {
        "id": _id_seq,
        "account_id": target["id"],
        "operation": "transfer_in",
        "amount": payload.amount,
        "created_at": now,
    }
    _id_seq += 1
    transactions_db.extend([tx_out, tx_in])

    return {
        "message": "Transfer successful",
        "source_balance": source["balance"],
        "target_balance": target["balance"],
    }
