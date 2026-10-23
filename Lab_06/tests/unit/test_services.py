from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from application.models import Account
from application.repositories import InMemoryAccountRepository
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


def test_notifier_mock_and_side_effect() -> None:
    mock_repo = MagicMock(spec=InMemoryAccountRepository)
    acc = Account("UA100", "C1", 500.0)
    mock_repo.get_by_id.return_value = acc

    mock_notifier = MagicMock(spec=Notifier)
    service = BankingService(repo=mock_repo, notifier=mock_notifier)

    service.deposit("UA100", 200.0)
    assert acc.balance == 700.0
    mock_notifier.notify.assert_called_once_with("Deposit 200.0 into UA100")

    # Notifier failure path via side_effect
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
