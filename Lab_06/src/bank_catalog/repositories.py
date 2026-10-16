from typing import Optional
from bank_catalog.models import AccountEntity


class AccountRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, AccountEntity] = {}

    def save(self, account: AccountEntity) -> None:
        self._accounts[account.account_number] = account

    def get_by_number(self, account_number: str) -> Optional[AccountEntity]:
        return self._accounts.get(account_number)

    def list_all(self) -> list[AccountEntity]:
        return list(self._accounts.values())
