from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from bank_storage.models import AccountModel, ClientModel, TransactionModel


class ClientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, full_name: str, email: str) -> ClientModel:
        client = ClientModel(full_name=full_name, email=email)
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def get_by_id(self, client_id: int) -> Optional[ClientModel]:
        return self.session.get(ClientModel, client_id)


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, client_id: int, account_number: str, initial_balance: float = 0.0) -> AccountModel:
        account = AccountModel(client_id=client_id, account_number=account_number, balance=initial_balance)
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def get_by_number(self, account_number: str) -> Optional[AccountModel]:
        stmt = select(AccountModel).where(AccountModel.account_number == account_number)
        return self.session.scalars(stmt).first()

    def list_all(self) -> list[AccountModel]:
        return list(self.session.scalars(select(AccountModel)).all())
