from __future__ import annotations

import sys

from bank_storage.database import Base, SessionLocal, engine
from bank_storage.repositories import AccountRepository, ClientRepository
from bank_storage.services import calculate_total_funds


def main() -> int:
    Base.metadata.create_all(engine)
    session = SessionLocal()
    try:
        c_repo = ClientRepository(session)
        a_repo = AccountRepository(session)

        client = c_repo.get_by_name("Artem Kyrychenko")
        if not client:
            client = c_repo.create("Artem Kyrychenko", "artem.bank@example.com")

        acc = a_repo.get_by_number("UA-MAIN-100")
        if not acc:
            acc = a_repo.create(client.id, "UA-MAIN-100", 5000.0)

        total = calculate_total_funds(session)
        print(f"Bank storage active. Total funds: {total:.2f}")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())
