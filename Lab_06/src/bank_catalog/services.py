from bank_catalog.models import AccountEntity
from bank_catalog.repositories import AccountRepository


class BankService:
    def __init__(self, repo: AccountRepository) -> None:
        self.repo = repo

    def open_account(self, account_number: str, client_id: str, initial_deposit: float = 0.0) -> AccountEntity:
        if self.repo.get_by_number(account_number):
            raise ValueError(f"Account {account_number} already exists")
        account = AccountEntity(account_number=account_number, client_id=client_id, balance=initial_deposit)
        self.repo.save(account)
        return account

    def transfer(self, from_num: str, to_num: str, amount: float) -> tuple[float, float]:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        source = self.repo.get_by_number(from_num)
        target = self.repo.get_by_number(to_num)
        if not source or not target:
            raise LookupError("One or both accounts missing")

        # Atomic debit and credit
        source.withdraw(amount)
        target.deposit(amount)
        return source.balance, target.balance
