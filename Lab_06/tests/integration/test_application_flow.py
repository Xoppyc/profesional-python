from __future__ import annotations

import pytest
from application.models import Account
from application.repositories import InMemoryAccountRepository
from application.services import BankingService


@pytest.mark.integration
def test_full_application_flow() -> None:
    repo = InMemoryAccountRepository()
    service = BankingService(repo)

    acc = Account("UA-FLOW-1", "C-FLOW", 1000.0)
    repo.save(acc)

    service.deposit("UA-FLOW-1", 500.0)
    assert acc.balance == 1500.0

    service.withdraw("UA-FLOW-1", 200.0)
    assert acc.balance == 1300.0
