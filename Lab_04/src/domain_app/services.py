from __future__ import annotations

from domain_app.models import Account, BankingError
from domain_app.protocols import Notifier
from domain_app.repositories import AccountRepository


class BankingService:
    def __init__(self, repo: AccountRepository, notifier: Notifier | None = None) -> None:
        self.repo = repo
        self.notifier = notifier

    def check_balance(self, account_number: str) -> float:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        return account.balance

    def find_account(self, account_number: str) -> Account | None:
        return self.repo.find_by_account_number(account_number)

    def calculate_total_funds(self) -> float:
        return self.repo.calculate_total_funds()

    def deposit(self, account_number: str, amount: float) -> None:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        account.deposit(amount)
        if self.notifier:
            self.notifier.notify(f"Deposited {amount} to {account_number}")

    def withdraw(self, account_number: str, amount: float) -> None:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        account.withdraw(amount)
        if self.notifier:
            self.notifier.notify(f"Withdrawn {amount} from {account_number}")

    def transfer(self, source_acc_num: str, target_acc_num: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")

        source = self.repo.get_by_id(source_acc_num)
        target = self.repo.get_by_id(target_acc_num)

        if not source or not target:
            raise BankingError("One or both accounts were not found")

        source.withdraw(amount)
        target.deposit(amount)
        if self.notifier:
            self.notifier.notify(f"Transferred {amount} from {source_acc_num} to {target_acc_num}")


AccountService = BankingService
AccountTransferService = BankingService
