from __future__ import annotations

import pytest
from application.models import Account, Customer, InsufficientFundsError
from application.services import classify_account_balance, classify_grade
from bank_catalog.models import AccountEntity


@pytest.mark.parametrize(
    "initial,deposit_amt,expected",
    [
        (100.0, 50.0, 150.0),
        (0.0, 1000.0, 1000.0),
        (500.0, 250.75, 750.75),
    ],
)
def test_parametrized_deposits(initial: float, deposit_amt: float, expected: float) -> None:
    acc = AccountEntity("UA1", "C1", initial)
    acc.deposit(deposit_amt)
    assert acc.balance == pytest.approx(expected)


def test_withdraw_limits() -> None:
    acc = AccountEntity("UA2", "C1", 200.0)
    with pytest.raises(ValueError, match="Insufficient balance"):
        acc.withdraw(250.0)

    acc.status = "blocked"
    with pytest.raises(PermissionError, match="inactive"):
        acc.deposit(100.0)


def test_account_creation_validation() -> None:
    account = Account("UA300", "CUST-1", 5000.0)
    assert account.account_number == "UA300"
    assert account.client_id == "CUST-1"
    assert account.check_balance() == pytest.approx(5000.0)


def test_account_deposit_success_and_approx() -> None:
    account = Account("UA301", "CUST-1", 100.0)
    account.deposit(50.25)
    assert account.check_balance() == pytest.approx(150.25)
    account.deposit(0.01)
    assert account.check_balance() == pytest.approx(150.26)


def test_account_deposit_invalid_values() -> None:
    account = Account("UA302", "CUST-1", 100.0)
    with pytest.raises(ValueError, match="strictly positive"):
        account.deposit(0.0)
    with pytest.raises(ValueError, match="strictly positive"):
        account.deposit(-25.0)


def test_account_withdraw_success_to_zero() -> None:
    account = Account("UA303", "CUST-1", 200.0)
    account.withdraw(200.0)
    assert account.check_balance() == pytest.approx(0.0)


def test_account_withdraw_insufficient_funds() -> None:
    account = Account("UA304", "CUST-1", 150.0)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(150.01)


def test_customer_entity_attributes() -> None:
    customer = Customer("CUST-9", "Artem Kyrychenko", "artem@example.com")
    assert customer.client_id == "CUST-9"
    assert customer.full_name == "Artem Kyrychenko"
    assert customer.email == "artem@example.com"


@pytest.mark.parametrize(
    "grade,expected",
    [
        (95.0, "excellent"),
        (90.0, "excellent"),
        (75.0, "passed"),
        (60.0, "passed"),
        (45.0, "failed"),
    ],
)
def test_classify_grade_branch_coverage(grade: float, expected: str) -> None:
    assert classify_grade(grade) == expected


@pytest.mark.parametrize(
    "balance,expected",
    [
        (15000.0, "premium"),
        (2500.0, "standard"),
        (500.0, "basic"),
    ],
)
def test_classify_account_balance(balance: float, expected: str) -> None:
    assert classify_account_balance(balance) == expected
