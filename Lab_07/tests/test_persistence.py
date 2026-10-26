from __future__ import annotations

import sqlite3
from collections.abc import Generator
from pathlib import Path

import pytest
from bank_storage.database import Base
from bank_storage.db_api import query_account_raw_db_api
from bank_storage.repositories import AccountRepository, ClientRepository, TransactionRepository
from bank_storage.services import (
    InsufficientBalanceError,
    NegativeAmountError,
    calculate_total_funds,
    deposit_money,
    transfer_money,
    withdraw_money,
)
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture
def db_session(tmp_path: Path) -> Generator[Session, None, None]:
    db_file = tmp_path / "test_bank.db"
    engine = create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_client_and_account_crud(db_session: Session) -> None:
    client_repo = ClientRepository(db_session)
    account_repo = AccountRepository(db_session)

    client = client_repo.create("Artem Kyrychenko", "zoom.2000v@gmail.com")
    assert client.id is not None
    assert client.full_name == "Artem Kyrychenko"

    account = account_repo.create(client.id, "UA7001", 1000.0)
    assert account.balance == 1000.0
    assert account.client_id == client.id

    retrieved = account_repo.get_by_number("UA7001")
    assert retrieved is not None
    assert retrieved.client.full_name == "Artem Kyrychenko"

    accounts = account_repo.list_all()
    assert len(accounts) >= 1

    account_repo.update_balance(account.id, 1500.0)
    assert account_repo.get_by_id(account.id).balance == 1500.0


def test_deposit_and_withdraw_services(db_session: Session) -> None:
    client_repo = ClientRepository(db_session)
    account_repo = AccountRepository(db_session)

    client = client_repo.create("Tester", "tester@bank.ua")
    account_repo.create(client.id, "UA-DW-1", 500.0)

    # Deposit
    new_bal = deposit_money(db_session, "UA-DW-1", 250.0)
    assert new_bal == 750.0

    # Withdraw
    new_bal = withdraw_money(db_session, "UA-DW-1", 100.0)
    assert new_bal == 650.0

    # Negative amount validation
    with pytest.raises(NegativeAmountError):
        deposit_money(db_session, "UA-DW-1", -50.0)

    with pytest.raises(NegativeAmountError):
        withdraw_money(db_session, "UA-DW-1", 0.0)

    # Overdraft attempt
    with pytest.raises(InsufficientBalanceError):
        withdraw_money(db_session, "UA-DW-1", 1000.0)


def test_negative_balance_constraint(db_session: Session) -> None:
    client_repo = ClientRepository(db_session)
    account_repo = AccountRepository(db_session)

    client = client_repo.create("Constraint User", "constraint@bank.ua")
    with pytest.raises(IntegrityError):
        account_repo.create(client.id, "UA-NEG", -10.0)
        db_session.flush()
    db_session.rollback()


def test_total_funds_calculation(db_session: Session) -> None:
    client_repo = ClientRepository(db_session)
    account_repo = AccountRepository(db_session)

    client = client_repo.create("Investor", "investor@bank.ua")
    account_repo.create(client.id, "UA-TOTAL-1", 1200.0)
    account_repo.create(client.id, "UA-TOTAL-2", 800.0)

    total = calculate_total_funds(db_session)
    assert total >= 2000.0


def test_transfer_money_success_and_rollback(db_session: Session) -> None:
    c_repo = ClientRepository(db_session)
    a_repo = AccountRepository(db_session)

    client = c_repo.create("User", "user@bank.ua")
    acc1 = a_repo.create(client.id, "UA-ACC-1", 500.0)
    acc2 = a_repo.create(client.id, "UA-ACC-2", 100.0)

    # Successful transfer
    b1, b2 = transfer_money(db_session, "UA-ACC-1", "UA-ACC-2", 200.0)
    assert b1 == 300.0
    assert b2 == 300.0

    # Failed transfer triggers rollback
    with pytest.raises(InsufficientBalanceError):
        transfer_money(db_session, "UA-ACC-1", "UA-ACC-2", 1000.0)

    # Ensure balances did not change on failure
    db_session.refresh(acc1)
    db_session.refresh(acc2)
    assert acc1.balance == 300.0
    assert acc2.balance == 300.0


def test_transaction_repository_history(db_session: Session) -> None:
    c_repo = ClientRepository(db_session)
    a_repo = AccountRepository(db_session)
    tx_repo = TransactionRepository(db_session)

    client = c_repo.create("History User", "history@bank.ua")
    acc = a_repo.create(client.id, "UA-HIST-1", 100.0)

    tx_repo.create(acc.id, "deposit", 50.0)
    tx_repo.create(acc.id, "withdraw", 20.0)

    history = tx_repo.list_by_account(acc.id)
    assert len(history) == 2
    assert history[0].operation == "deposit"
    assert history[1].operation == "withdraw"


def test_raw_db_api_query(tmp_path: Path) -> None:
    db_file = tmp_path / "raw_db_test.db"
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE accounts (id INTEGER PRIMARY KEY, account_number TEXT, balance REAL, client_id INTEGER)"
    )
    cursor.execute(
        "INSERT INTO accounts (account_number, balance, client_id) VALUES (?, ?, ?)",
        ("UA-RAW-100", 3500.0, 1),
    )
    conn.commit()
    conn.close()

    result = query_account_raw_db_api(str(db_file), "UA-RAW-100")
    assert result is not None
    assert result["account_number"] == "UA-RAW-100"
    assert result["balance"] == 3500.0

    not_found = query_account_raw_db_api(str(db_file), "UA-NONEXISTENT")
    assert not_found is None
