from __future__ import annotations

import pytest
from application.models import Account, InsufficientFundsError


def test_deposit_boundary_and_invalid_amount() -> None:
    acc = Account("UA100", "CUST1", 100.0)
    with pytest.raises(ValueError, match="strictly positive"):
        acc.deposit(0.0)
    with pytest.raises(ValueError, match="strictly positive"):
        acc.deposit(-50.0)

    acc.deposit(0.01)
    assert acc.balance == 100.01


def test_withdraw_boundary_and_overdraft() -> None:
    acc = Account("UA100", "CUST1", 100.0)
    with pytest.raises(ValueError, match="strictly positive"):
        acc.withdraw(0.0)
    with pytest.raises(ValueError, match="strictly positive"):
        acc.withdraw(-10.0)

    # Valid boundary withdrawal to zero
    acc.withdraw(100.0)
    assert acc.balance == 0.0

    # Overdraft rejected
    with pytest.raises(InsufficientFundsError):
        acc.withdraw(0.01)


def test_inactive_account_prohibits_mutations() -> None:
    blocked = Account("UA999", "CUST1", 500.0, status="blocked")
    with pytest.raises(PermissionError):
        blocked.deposit(100.0)
    with pytest.raises(PermissionError):
        blocked.withdraw(50.0)
