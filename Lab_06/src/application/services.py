from __future__ import annotations

from typing import Protocol

from application.models import Account, BankingError
from application.repositories import InMemoryAccountRepository


def classify_grade(grade: float) -> str:
    if grade >= 90.0:
        return "excellent"
    if grade >= 60.0:
        return "passed"
    return "failed"


def classify_account_balance(balance: float) -> str:
    if balance >= 10000.0:
        return "premium"
    if balance >= 1000.0:
        return "standard"
    return "basic"


class Notifier(Protocol):
    def notify(self, message: str) -> None: ...
    def send(self, message: str) -> None: ...


class AsyncLedgerClient(Protocol):
    async def fetch_remote_balance(self, account_number: str) -> float: ...


class BankingService:
    def __init__(
        self,
        repo: InMemoryAccountRepository,
        notifier: Notifier | None = None,
        async_client: AsyncLedgerClient | None = None,
    ) -> None:
        self.repo = repo
        self.notifier = notifier
        self.async_client = async_client

    def deposit(self, account_number: str, amount: float) -> None:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        account.deposit(amount)
        if self.notifier:
            self.notifier.notify(f"Deposit {amount} into {account_number}")

    def withdraw(self, account_number: str, amount: float) -> None:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        account.withdraw(amount)
        if self.notifier:
            self.notifier.notify(f"Withdrawal {amount} from {account_number}")

    def transfer(self, source_acc: str, target_acc: str, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be strictly positive")
        src = self.repo.get_by_id(source_acc)
        tgt = self.repo.get_by_id(target_acc)
        if not src or not tgt:
            raise BankingError("One or both transfer accounts not found")

        src.withdraw(amount)
        tgt.deposit(amount)
        if self.notifier:
            self.notifier.notify(f"Transferred {amount} from {source_acc} to {target_acc}")

    def check_balance(self, account_number: str) -> float:
        account = self.repo.get_by_id(account_number)
        if not account:
            raise BankingError(f"Account {account_number} not found")
        return account.check_balance()

    def find_account(self, account_number: str) -> Account | None:
        return self.repo.find_by_account_number(account_number)

    def calculate_total_funds(self) -> float:
        return self.repo.calculate_total_funds()

    async def sync_with_remote_ledger(self, account_number: str) -> float:
        if not self.async_client:
            raise RuntimeError("Async ledger client not configured")
        remote_bal = await self.async_client.fetch_remote_balance(account_number)
        account = self.repo.get_by_id(account_number)
        if account:
            account.balance = remote_bal
        return remote_bal


AccountService = BankingService
