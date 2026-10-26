from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Self

AccountStatus = Literal["active", "blocked", "closed"]


class BankingError(Exception):
    """Base banking domain exception."""


class InsufficientFundsError(BankingError):
    """Raised when withdrawal produces negative balance."""


class DataImportError(Exception):
    """Raised when data import parsing fails."""


def parse_value(text: str) -> int:
    try:
        return int(text)
    except ValueError as error:
        raise DataImportError("Invalid value") from error


class CustomResource:
    def __init__(self) -> None:
        self.is_open: bool = False

    def __enter__(self) -> Self:
        self.is_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.is_open = False


@dataclass(slots=True, frozen=True)
class Customer:
    client_id: str
    full_name: str
    email: str


ClientEntity = Customer


@dataclass(slots=True)
class Account:
    account_number: str
    client_id: str
    balance: float
    status: AccountStatus = "active"

    def deposit(self, amount: float) -> None:
        if self.status != "active":
            raise PermissionError("Cannot deposit into inactive account")
        if amount <= 0:
            raise ValueError("Deposit amount must be strictly positive")
        self.balance = round(self.balance + amount, 2)

    def withdraw(self, amount: float) -> None:
        if self.status != "active":
            raise PermissionError("Cannot withdraw from inactive account")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be strictly positive")
        if self.balance < amount:
            raise InsufficientFundsError(
                f"Insufficient funds: withdrawal of {amount} exceeds balance {self.balance}"
            )
        self.balance = round(self.balance - amount, 2)

    def check_balance(self) -> float:
        return self.balance


AccountEntity = Account
