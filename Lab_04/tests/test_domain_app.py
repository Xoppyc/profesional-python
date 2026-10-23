from __future__ import annotations

import pytest
from domain_app.models import (
    Account,
    CurrentAccount,
    Customer,
    InsufficientFundsError,
    SavingsAccount,
    Transaction,
)
from domain_app.repositories import AccountRepository
from domain_app.services import BankingService


@pytest.fixture
def customer() -> Customer:
    return Customer("CUST1", "Artem Kyrychenko", "artem@example.com")


def test_account_prohibits_negative_balance(customer: Customer) -> None:
    class BasicAccount(Account):
        pass

    acc = BasicAccount("UA100", customer, initial_balance=200.0)
    acc.deposit(100.0)
    assert acc.balance == 300.0
    assert acc.check_balance() == 300.0

    acc.withdraw(250.0)
    assert acc.balance == 50.0

    with pytest.raises(InsufficientFundsError):
        acc.withdraw(100.0)


def test_banking_service_and_repository(customer: Customer) -> None:
    repo = AccountRepository()
    service = BankingService(repo=repo)

    acc1 = SavingsAccount("UA101", customer, initial_balance=1000.0)
    acc2 = CurrentAccount("UA102", customer, initial_balance=500.0)

    repo.add(acc1)
    repo.add(acc2)

    assert service.check_balance("UA101") == 1000.0
    assert service.find_account("UA102") is not None
    assert service.calculate_total_funds() == 1500.0

    service.transfer("UA101", "UA102", 300.0)
    assert acc1.balance == 700.0
    assert acc2.balance == 800.0
    assert service.calculate_total_funds() == 1500.0


def test_transaction_model() -> None:
    tx = Transaction(
        transaction_id="TX100",
        account_number="UA101",
        amount=500.0,
        operation_type="deposit",
    )
    assert tx.transaction_id == "TX100"
    assert tx.amount == 500.0

