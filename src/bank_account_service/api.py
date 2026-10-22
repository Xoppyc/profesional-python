from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from bank_account_service.database import Base, engine, get_db
from bank_account_service.repositories import BankRepository
from bank_account_service.schemas import (
    AccountCreate,
    AccountResponse,
    AmountRequest,
    ClientCreate,
    ClientResponse,
    TransactionResponse,
    TransferRequest,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bank Account Service", version="1.0.0")

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
def health_status() -> dict[str, str]:
    return {"status": "ok", "service": "bank-account-service"}


@app.post("/clients", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(payload: ClientCreate, db: DbSession) -> ClientResponse:
    repo = BankRepository(db)
    return repo.create_client(payload.full_name, payload.email)  # type: ignore[return-value]


@app.post("/accounts", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreate, db: DbSession) -> AccountResponse:
    repo = BankRepository(db)
    if not repo.get_client(payload.client_id):
        raise HTTPException(status_code=404, detail="Client not found")
    return repo.create_account(payload.client_id, payload.account_number, payload.initial_balance)  # type: ignore[return-value]


@app.get("/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int, db: DbSession) -> AccountResponse:
    repo = BankRepository(db)
    account = repo.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account  # type: ignore[return-value]


@app.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
def get_transactions(account_id: int, db: DbSession) -> list[TransactionResponse]:
    repo = BankRepository(db)
    if not repo.get_account_by_id(account_id):
        raise HTTPException(status_code=404, detail="Account not found")
    return repo.list_account_transactions(account_id)  # type: ignore[return-value]


@app.post("/accounts/{account_id}/deposit", response_model=AccountResponse)
def deposit(account_id: int, payload: AmountRequest, db: DbSession) -> AccountResponse:
    repo = BankRepository(db)
    account = repo.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    account.balance += payload.amount
    repo.record_transaction(account_id, "deposit", payload.amount)
    db.commit()
    db.refresh(account)
    return account  # type: ignore[return-value]


@app.post("/accounts/{account_id}/withdraw", response_model=AccountResponse)
def withdraw(account_id: int, payload: AmountRequest, db: DbSession) -> AccountResponse:
    repo = BankRepository(db)
    account = repo.get_account_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if account.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    account.balance -= payload.amount
    repo.record_transaction(account_id, "withdraw", payload.amount)
    db.commit()
    db.refresh(account)
    return account  # type: ignore[return-value]


@app.post("/transfers", status_code=status.HTTP_200_OK)
def transfer(payload: TransferRequest, db: DbSession) -> dict:
    repo = BankRepository(db)
    source = repo.get_account_by_id(payload.source_account_id)
    target = repo.get_account_by_id(payload.target_account_id)

    if not source or not target:
        raise HTTPException(status_code=404, detail="Account not found")
    if source.balance < payload.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Atomic double-entry transfer with transaction log
    source.balance -= payload.amount
    target.balance += payload.amount
    repo.record_transaction(source.id, "transfer_out", payload.amount)
    repo.record_transaction(target.id, "transfer_in", payload.amount)
    db.commit()
    return {"status": "success", "source_balance": source.balance, "target_balance": target.balance}
