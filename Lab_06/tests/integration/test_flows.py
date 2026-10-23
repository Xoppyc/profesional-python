from __future__ import annotations

import pytest
from bank_catalog.services import BankService


@pytest.mark.integration
def test_full_banking_workflow_integration(bank_service: BankService) -> None:
    # 1. Open two accounts
    acc_a = bank_service.open_account("UA-ACC-101", "C-1", 5000.0)
    acc_b = bank_service.open_account("UA-ACC-102", "C-2", 1000.0)

    # 2. Perform valid transfer
    b1, b2 = bank_service.transfer("UA-ACC-101", "UA-ACC-102", 2000.0)
    assert b1 == 3000.0
    assert b2 == 3000.0

    # 3. Attempt transfer exceeding balance
    with pytest.raises(ValueError, match="Insufficient balance"):
        bank_service.transfer("UA-ACC-101", "UA-ACC-102", 4000.0)

    # 4. Verify balances remain unchanged after failed transaction
    assert acc_a.balance == 3000.0
    assert acc_b.balance == 3000.0
