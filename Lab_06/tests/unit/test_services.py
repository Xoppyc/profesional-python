from unittest.mock import MagicMock

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
