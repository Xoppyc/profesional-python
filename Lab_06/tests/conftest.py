from __future__ import annotations

from collections.abc import Generator

import pytest
from application.models import Account, Customer
from application.repositories import InMemoryAccountRepository
from application.services import BankingService
from bank_catalog.models import ClientEntity
from bank_catalog.repositories import AccountRepository
from bank_catalog.services import BankService
from shop.models import Cart, Product
from shop.value_objects import Money


@pytest.fixture
def product_factory():
    def create_product(
        *,
        product_id: int = 1,
        name: str = "Product",
        price: float = 100,
    ) -> Product:
        return Product(
            product_id=product_id,
            name=name,
            price=Money(price),
        )

    return create_product


@pytest.fixture
def laptop() -> Product:
    return Product(
        product_id=1,
        name="Laptop",
        price=Money(35_000),
    )


@pytest.fixture
def mouse() -> Product:
    return Product(
        product_id=2,
        name="Mouse",
        price=Money(1_200),
    )


@pytest.fixture
def cart(laptop: Product, mouse: Product) -> Cart:
    c = Cart()
    c.add(laptop, 1)
    c.add(mouse, 2)
    return c


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
def managed_account() -> Generator[Account, None, None]:
    acc = Account("UA-YIELD-1", "CUST-Y", 1000.0)
    yield acc
    acc.balance = 0.0


@pytest.fixture
def account_repo() -> InMemoryAccountRepository:
    return InMemoryAccountRepository()


@pytest.fixture
def banking_service(account_repo: InMemoryAccountRepository) -> BankingService:
    return BankingService(account_repo)
