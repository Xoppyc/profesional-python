from __future__ import annotations

import pytest
from bank_storage.models import AccountModel, ClientModel
from bank_storage.repositories import AccountRepository, ClientRepository
from bank_storage.services import InsufficientBalanceError, transfer_money
from sqlalchemy.orm import Session


def test_add_client(session: Session) -> None:
    client_repo = ClientRepository(session)
    client = ClientModel(full_name="Artem Kyrychenko", email="artem@bank.ua")
    saved = client_repo.add(client)
    assert saved.id is not None
    assert saved.full_name == "Artem Kyrychenko"


def test_add_account(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("John Doe", "john@bank.ua")
    account = AccountModel(client_id=client.id, account_number="UA-REPO-1", balance=1500.0)
    saved = account_repo.add(account)

    assert saved.id is not None
    assert saved.balance == 1500.0
    assert saved.account_number == "UA-REPO-1"


def test_get_account(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("Jane Doe", "jane@bank.ua")
    account = account_repo.create(client.id, "UA-REPO-2", 2500.0)

    found = account_repo.get_by_id(account.id)
    assert found is not None
    assert found.account_number == "UA-REPO-2"

    found_by_num = account_repo.get_by_number("UA-REPO-2")
    assert found_by_num is not None
    assert found_by_num.id == account.id


def test_update_balance(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("Alice", "alice@bank.ua")
    account = account_repo.create(client.id, "UA-REPO-3", 300.0)

    updated = account_repo.update_balance(account.id, 900.0)
    assert updated is not None
    assert updated.balance == 900.0


def test_delete_account(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("Bob", "bob@bank.ua")
    account = account_repo.create(client.id, "UA-REPO-4", 50.0)

    deleted = account_repo.delete(account.id)
    assert deleted is True
    assert account_repo.get_by_id(account.id) is None


def test_total_funds(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("Charlie", "charlie@bank.ua")
    account_repo.create(client.id, "UA-TF-1", 1000.0)
    account_repo.create(client.id, "UA-TF-2", 2000.0)

    assert account_repo.total_funds() >= 3000.0


def test_transfer_rollback(session: Session) -> None:
    client_repo = ClientRepository(session)
    account_repo = AccountRepository(session)

    client = client_repo.create("David", "david@bank.ua")
    acc1 = account_repo.create(client.id, "UA-TR-1", 400.0)
    acc2 = account_repo.create(client.id, "UA-TR-2", 100.0)

    with pytest.raises(InsufficientBalanceError):
        transfer_money(session, "UA-TR-1", "UA-TR-2", 900.0)

    session.refresh(acc1)
    session.refresh(acc2)
    assert acc1.balance == 400.0
    assert acc2.balance == 100.0
