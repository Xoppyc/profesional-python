from __future__ import annotations

from collections.abc import Generator

import pytest
from bank_storage.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


@pytest.fixture
def session() -> Generator[Session, None, None]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestSession() as sess:
        yield sess
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(session: Session) -> Session:
    return session
