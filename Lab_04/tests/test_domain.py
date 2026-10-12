import pytest
from bank_domain.models import (
    CurrentAccount,
    Customer,
    InsufficientFundsError,
    OverdraftLimitExceededError,
    SavingsAccount,
)
from bank_domain.repository import InMemoryRepository
from bank_domain.services import AccountTransferService


@pytest.fixture
def sample_customer() -> Customer:
    return Customer(customer_id="CUST-1", full_name="Artem Kyrychenko", email="zoom.2000v@gmail.com")


def test_savings_account_reserve(sample_customer: Customer) -> None:
    savings = SavingsAccount("UA-SAV-1", sample_customer, initial_balance=500.0, min_reserve=100.0)
    savings.withdraw(350.0)
    assert savings.balance == 150.0

    with pytest.raises(InsufficientFundsError):
        savings.withdraw(60.0)


def test_current_account_overdraft(sample_customer: Customer) -> None:
    current = CurrentAccount("UA-CUR-1", sample_customer, initial_balance=200.0, overdraft_limit=1000.0)
    current.withdraw(800.0)
    assert current.balance == -600.0

    with pytest.raises(OverdraftLimitExceededError):
        current.withdraw(500.0)


def test_transfer_service_success(sample_customer: Customer) -> None:
    repo = InMemoryRepository()
    acc1 = CurrentAccount("UA-A", sample_customer, initial_balance=1000.0)
    acc2 = SavingsAccount("UA-B", sample_customer, initial_balance=200.0, min_reserve=50.0)
    repo.add(acc1)
    repo.add(acc2)

    service = AccountTransferService(repo)
    service.transfer("UA-A", "UA-B", 400.0)

    assert acc1.balance == 600.0
    assert acc2.balance == 600.0
