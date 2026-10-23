from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from application.models import Account, BankingError
from application.repositories import FakeRepository, InMemoryAccountRepository
from application.services import AsyncLedgerClient, BankingService, Notifier
from bank_catalog.models import AccountEntity
from bank_catalog.repositories import AccountRepository
from bank_catalog.services import BankService


def test_transfer_with_mock_repository() -> None:
    mock_repo = MagicMock(spec=AccountRepository)
    acc1 = AccountEntity("UA-1", "C1", 1000.0)
    acc2 = AccountEntity("UA-2", "C2", 500.0)

    mock_repo.get_by_number.side_effect = lambda num: {"UA-1": acc1, "UA-2": acc2}.get(num)

    service = BankService(mock_repo)
    b1, b2 = service.transfer("UA-1", "UA-2", 300.0)

    assert b1 == 700.0
    assert b2 == 800.0
    assert mock_repo.get_by_number.call_count == 2


def test_find_account_and_check_balance() -> None:
    repo = InMemoryAccountRepository()
    acc = Account("UA100", "C1", 2500.0)
    repo.add(acc)
    service = BankingService(repo)

    found = service.find_account("UA100")
    assert found is not None
    assert found.account_number == "UA100"
    assert service.check_balance("UA100") == 2500.0


def test_find_account_not_found() -> None:
    repo = InMemoryAccountRepository()
    service = BankingService(repo)
    assert service.find_account("NON_EXISTING") is None
    with pytest.raises(BankingError, match="not found"):
        service.check_balance("NON_EXISTING")


def test_calculate_total_funds() -> None:
    repo = InMemoryAccountRepository()
    repo.add(Account("UA1", "C1", 100.0))
    repo.add(Account("UA2", "C2", 250.50))
    repo.add(Account("UA3", "C3", 49.50))
    service = BankingService(repo)
    assert service.calculate_total_funds() == 400.0


def test_transfer_service_double_entry_success() -> None:
    repo = InMemoryAccountRepository()
    acc1 = Account("UA1", "C1", 1000.0)
    acc2 = Account("UA2", "C2", 200.0)
    repo.add(acc1)
    repo.add(acc2)

    service = BankingService(repo)
    service.transfer("UA1", "UA2", 300.0)
    assert acc1.check_balance() == 700.0
    assert acc2.check_balance() == 500.0


def test_transfer_service_invalid_amount() -> None:
    repo = InMemoryAccountRepository()
    service = BankingService(repo)
    with pytest.raises(ValueError, match="strictly positive"):
        service.transfer("UA1", "UA2", -50.0)


def test_notifier_mock_and_side_effect() -> None:
    mock_repo = MagicMock(spec=InMemoryAccountRepository)
    acc = Account("UA100", "C1", 500.0)
    mock_repo.get_by_id.return_value = acc

    mock_notifier = MagicMock(spec=Notifier)
    service = BankingService(repo=mock_repo, notifier=mock_notifier)

    service.deposit("UA100", 200.0)
    assert acc.balance == 700.0
    mock_notifier.notify.assert_called_once_with("Deposit 200.0 into UA100")

    mock_notifier.notify.side_effect = ConnectionError("SMS gateway timeout")
    with pytest.raises(ConnectionError, match="SMS gateway timeout"):
        service.deposit("UA100", 50.0)


@pytest.mark.anyio
async def test_async_ledger_dependency_with_async_mock() -> None:
    mock_repo = MagicMock(spec=InMemoryAccountRepository)
    acc = Account("UA100", "C1", 500.0)
    mock_repo.get_by_id.return_value = acc

    mock_async_client = AsyncMock(spec=AsyncLedgerClient)
    mock_async_client.fetch_remote_balance.return_value = 12500.75

    service = BankingService(repo=mock_repo, async_client=mock_async_client)
    synced_balance = await service.sync_with_remote_ledger("UA100")

    assert synced_balance == 12500.75
    assert acc.balance == 12500.75
    mock_async_client.fetch_remote_balance.assert_awaited_once_with("UA100")


def test_fake_repository_crud() -> None:
    fake_repo = FakeRepository()
    acc = Account("UA777", "CUST7", 900.0)
    fake_repo.add(acc)

    assert fake_repo.get_by_id("UA777") == acc
    assert len(fake_repo.list_all()) == 1
    assert fake_repo.delete("UA777") is True
    assert fake_repo.get_by_id("UA777") is None
