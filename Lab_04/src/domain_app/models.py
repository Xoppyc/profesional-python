from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


class BankingError(Exception):
    """Base exception for domain banking errors."""


class InsufficientFundsError(BankingError):
    """Raised when an account does not have sufficient balance for withdrawal."""


class OverdraftLimitExceededError(BankingError):
    """Raised when an account exceeds its authorized credit line."""


@dataclass(slots=True, frozen=True)
class Customer:
    customer_id: str
    full_name: str
    email: str


@dataclass(slots=True, frozen=True)
class Transaction:
    transaction_id: str
    account_number: str
    amount: float
    operation_type: str
    timestamp: datetime = field(default_factory=datetime.now)


TransactionRecord = Transaction


class Account(ABC):
    def __init__(
        self, account_number: str, customer: Customer, initial_balance: float = 0.0
    ) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._account_number = account_number
        self._customer = customer
        self._balance = round(initial_balance, 2)

    @property
    def identifier(self) -> str:
        return self._account_number

    @property
    def account_number(self) -> str:
        return self._account_number

    @property
    def customer(self) -> Customer:
        return self._customer

    @property
    def balance(self) -> float:
        return self._balance

    def check_balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance = round(self._balance + amount, 2)

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        # Enforce non-negative ledger balance to maintain double-entry integrity
        if self._balance - amount < 0:
            raise InsufficientFundsError("Insufficient funds: negative balance prohibited")
        self._balance = round(self._balance - amount, 2)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._account_number} balance={self._balance:.2f}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Account):
            return False
        return self._account_number == other._account_number

    def __lt__(self, other: Account) -> bool:
        return self._balance < other._balance


BaseAccount = Account


class SavingsAccount(Account):
    def __init__(
        self,
        account_number: str,
        customer: Customer,
        initial_balance: float = 0.0,
        annual_interest_rate: float = 0.05,
        min_reserve: float = 100.0,
    ) -> None:
        super().__init__(account_number, customer, initial_balance)
        self.interest_rate = annual_interest_rate
        self.min_reserve = min_reserve

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self._balance - amount < self.min_reserve:
            raise InsufficientFundsError(f"Cannot breach minimum reserve of {self.min_reserve}")
        self._balance = round(self._balance - amount, 2)

    def apply_monthly_interest(self) -> float:
        accrual = round(self._balance * (self.interest_rate / 12.0), 2)
        self._balance = round(self._balance + accrual, 2)
        return accrual


class CurrentAccount(Account):
    def __init__(
        self,
        account_number: str,
        customer: Customer,
        initial_balance: float = 0.0,
        overdraft_limit: float = 5000.0,
    ) -> None:
        super().__init__(account_number, customer, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self._balance - amount < -self.overdraft_limit:
            raise OverdraftLimitExceededError(
                f"Withdrawal breaches authorized overdraft of {self.overdraft_limit}"
            )
        self._balance = round(self._balance - amount, 2)
