from collections.abc import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from bank_storage.database import Base
from bank_storage.models import AccountModel, ClientModel
from bank_storage.repositories import AccountRepository, ClientRepository
from bank_storage.services import InsufficientBalanceError, transfer_money


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_client_and_account_crud(db_session: Session) -> None:
    client_repo = ClientRepository(db_session)
    account_repo = AccountRepository(db_session)

    client = client_repo.create("Artem Kyrychenko", "zoom.2000v@gmail.com")
    assert client.id is not None

    account = account_repo.create(client.id, "UA7001", 1000.0)
    assert account.balance == 1000.0

    retrieved = account_repo.get_by_number("UA7001")
    assert retrieved is not None
    assert retrieved.client.full_name == "Artem Kyrychenko"


def test_transfer_money_success_and_rollback(db_session: Session) -> None:
    c_repo = ClientRepository(db_session)
    a_repo = AccountRepository(db_session)

    client = c_repo.create("User", "user@bank.ua")
    acc1 = a_repo.create(client.id, "UA-ACC-1", 500.0)
    acc2 = a_repo.create(client.id, "UA-ACC-2", 100.0)

    # Successful transfer
    b1, b2 = transfer_money(db_session, "UA-ACC-1", "UA-ACC-2", 200.0)
    assert b1 == 300.0
    assert b2 == 300.0

    # Failed transfer triggers rollback
    with pytest.raises(InsufficientBalanceError):
        transfer_money(db_session, "UA-ACC-1", "UA-ACC-2", 1000.0)

    # Ensure balances did not change on failure
    db_session.refresh(acc1)
    db_session.refresh(acc2)
    assert acc1.balance == 300.0
    assert acc2.balance == 300.0
