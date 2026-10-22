from sqlalchemy import select
from sqlalchemy.orm import Session

from bank_account_service.models import Account, Client, Transaction


class BankRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_client(self, full_name: str, email: str) -> Client:
        client = Client(full_name=full_name, email=email)
        self.db.add(client)
        self.db.commit()
        self.db.refresh(client)
        return client

    def get_client(self, client_id: int) -> Client | None:
        return self.db.get(Client, client_id)

    def create_account(
        self, client_id: int, account_number: str, initial_balance: float
    ) -> Account:
        account = Account(
            client_id=client_id, account_number=account_number, balance=initial_balance
        )
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)
        return account

    def get_account_by_id(self, account_id: int) -> Account | None:
        return self.db.get(Account, account_id)

    def list_accounts(self) -> list[Account]:
        return list(self.db.scalars(select(Account)).all())

    def record_transaction(self, account_id: int, operation: str, amount: float) -> Transaction:
        tx = Transaction(account_id=account_id, operation=operation, amount=amount)
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def list_account_transactions(self, account_id: int) -> list[Transaction]:
        stmt = (
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.id.desc())
        )
        return list(self.db.scalars(stmt).all())
