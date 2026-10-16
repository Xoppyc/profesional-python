from dataclasses import dataclass
from typing import Literal

AccountStatus = Literal["active", "blocked", "closed"]


@dataclass(slots=True, frozen=True)
class ClientEntity:
    client_id: str
    full_name: str
    email: str


@dataclass(slots=True)
class AccountEntity:
    account_number: str
    client_id: str
    balance: float
    status: AccountStatus = "active"

    def deposit(self, amount: float) -> None:
        if self.status != "active":
            raise PermissionError("Cannot deposit into inactive account")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if self.status != "active":
            raise PermissionError("Cannot withdraw from inactive account")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
