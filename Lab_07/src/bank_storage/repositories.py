from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from bank_storage.models import AccountModel, ClientModel, TransactionModel


class ClientRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, client: ClientModel) -> ClientModel:
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return client

    def create(self, full_name: str, email: str) -> ClientModel:
        client = ClientModel(full_name=full_name, email=email)
        return self.add(client)

    def get_by_id(self, client_id: int) -> ClientModel | None:
        return self.session.get(ClientModel, client_id)

    def get_by_name(self, full_name: str) -> ClientModel | None:
        stmt = select(ClientModel).where(ClientModel.full_name == full_name)
        return self.session.scalars(stmt).first()

    def get_all(self) -> list[ClientModel]:
        return list(self.session.scalars(select(ClientModel)).all())

    list_all = get_all

    def update(self, client: ClientModel) -> ClientModel:
        self.session.commit()
        self.session.refresh(client)
        return client

    def delete(self, client_id: int) -> bool:
        client = self.get_by_id(client_id)
        if client:
            self.session.delete(client)
            self.session.commit()
            return True
        return False


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, account: AccountModel) -> AccountModel:
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def create(
        self, client_id: int, account_number: str, initial_balance: float = 0.0
    ) -> AccountModel:
        account = AccountModel(
            client_id=client_id, account_number=account_number, balance=initial_balance
        )
        return self.add(account)

    def get_by_number(self, account_number: str) -> AccountModel | None:
        stmt = select(AccountModel).where(AccountModel.account_number == account_number)
        return self.session.scalars(stmt).first()

    def get_by_id(self, account_id: int) -> AccountModel | None:
        return self.session.get(AccountModel, account_id)

    def get_all(self) -> list[AccountModel]:
        return list(self.session.scalars(select(AccountModel)).all())

    list_all = get_all

    def update(self, account: AccountModel) -> AccountModel:
        self.session.commit()
        self.session.refresh(account)
        return account

    def update_balance(self, account_id: int, new_balance: float) -> AccountModel | None:
        account = self.get_by_id(account_id)
        if account:
            account.balance = new_balance
            self.session.commit()
            self.session.refresh(account)
        return account

    def delete(self, account_id: int) -> bool:
        account = self.get_by_id(account_id)
        if account:
            self.session.delete(account)
            self.session.commit()
            return True
        return False

    def total_funds(self) -> float:
        result = self.session.scalar(select(func.sum(AccountModel.balance)))
        return float(result or 0.0)


class TransactionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, tx: TransactionModel) -> TransactionModel:
        self.session.add(tx)
        self.session.commit()
        self.session.refresh(tx)
        return tx

    def create(self, account_id: int, operation: str, amount: float) -> TransactionModel:
        tx = TransactionModel(account_id=account_id, operation=operation, amount=amount)
        return self.add(tx)

    def get_all(self) -> list[TransactionModel]:
        return list(self.session.scalars(select(TransactionModel)).all())

    list_all = get_all

    def list_by_account(self, account_id: int) -> list[TransactionModel]:
        stmt = (
            select(TransactionModel)
            .where(TransactionModel.account_id == account_id)
            .order_by(TransactionModel.id)
        )
        return list(self.session.scalars(stmt).all())
