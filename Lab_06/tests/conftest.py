from typing import Generator
import pytest
from bank_catalog.models import AccountEntity, ClientEntity
from bank_catalog.repositories import AccountRepository
from bank_catalog.services import BankService


@pytest.fixture
def sample_client() -> ClientEntity:
    return ClientEntity(client_id="C-101", full_name="Artem Kyrychenko", email="zoom.2000v@gmail.com")


@pytest.fixture
def bank_repo() -> AccountRepository:
    return AccountRepository()


@pytest.fixture
def bank_service(bank_repo: AccountRepository) -> BankService:
    return BankService(bank_repo)
