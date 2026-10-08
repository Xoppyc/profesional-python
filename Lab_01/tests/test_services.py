import pytest
from bank_manager.models import Account
from bank_manager.services import (
    calculate_total_balance,
    create_account,
    deposit,
    filter_by_min_balance,
    find_by_account_number,
    find_largest_account,
    get_balance,
    withdraw,
)


@pytest.fixture
def sample_accounts() -> list[Account]:
    return [
        Account(account_number="UA101", client_name="Alice", balance=1000.0),
        Account(account_number="UA102", client_name="Bob", balance=2500.0),
    ]


def test_create_account(sample_accounts: list[Account]) -> None:
    new_acc = create_account(sample_accounts, "UA103", "Charlie", 500.0)
    assert new_acc.account_number == "UA103"
    assert len(sample_accounts) == 3


def test_deposit(sample_accounts: list[Account]) -> None:
    acc = deposit(sample_accounts, "UA101", 300.0)
    assert acc.balance == 1300.0


def test_withdraw_success(sample_accounts: list[Account]) -> None:
    acc = withdraw(sample_accounts, "UA101", 400.0)
    assert acc.balance == 600.0


def test_withdraw_insufficient_funds_rejected(sample_accounts: list[Account]) -> None:
    with pytest.raises(ValueError, match="Insufficient funds"):
        withdraw(sample_accounts, "UA101", 1500.0)


def test_negative_balance_instantiation_rejected() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        Account(account_number="UA999", client_name="Dave", balance=-50.0)


def test_aggregations(sample_accounts: list[Account]) -> None:
    assert calculate_total_balance(sample_accounts) == 3500.0
    largest = find_largest_account(sample_accounts)
    assert largest is not None
    assert largest.account_number == "UA102"
