from __future__ import annotations

import pytest
from application.models import Account, Customer
from application.repositories import InMemoryAccountRepository
from application.services import BankingService
from bank_catalog.models import ClientEntity
from bank_catalog.repositories import AccountRepository
from bank_catalog.services import BankService


@pytest.fixture
def sample_client() -> ClientEntity:
    return ClientEntity(
        client_id="C-101", full_name="Artem Kyrychenko", email="zoom.2000v@gmail.com"
    )


@pytest.fixture
def bank_repo() -> AccountRepository:
    return AccountRepository()


@pytest.fixture
def bank_service(bank_repo: AccountRepository) -> BankService:
    return BankService(bank_repo)


@pytest.fixture
def sample_customer() -> Customer:
    return Customer(client_id="C-101", full_name="Artem Kyrychenko", email="artem@example.com")


@pytest.fixture
def sample_account(sample_customer: Customer) -> Account:
    return Account(
        account_number="UA1001",
        client_id=sample_customer.client_id,
        balance=1000.0,
        status="active",
    )


@pytest.fixture
def account_repo() -> InMemoryAccountRepository:
    return InMemoryAccountRepository()


@pytest.fixture
def banking_service(account_repo: InMemoryAccountRepository) -> BankingService:
    return BankingService(account_repo)
