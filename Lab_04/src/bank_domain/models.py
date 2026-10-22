from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


class BankingError(Exception):
    pass


class InsufficientFundsError(BankingError):
    pass


class OverdraftLimitExceededError(BankingError):
    pass


@dataclass(slots=True, frozen=True)
class Customer:
    customer_id: str
    full_name: str
    email: str


@dataclass(slots=True, frozen=True)
class TransactionRecord:
    transaction_id: str
    account_number: str
    amount: float
    operation_type: str
    timestamp: datetime


class BaseAccount(ABC):
    def __init__(
        self, account_number: str, customer: Customer, initial_balance: float = 0.0
    ) -> None:
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self._account_number = account_number
        self._customer = customer
        self._balance = initial_balance

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

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: float) -> None: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self._account_number} balance={self._balance:.2f}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseAccount):
            return False
        return self._account_number == other._account_number

    def __lt__(self, other: "BaseAccount") -> bool:
        return self._balance < other._balance


class SavingsAccount(BaseAccount):
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
        # Enforce statutory minimum reserve on interest-bearing accounts
        if self._balance - amount < self.min_reserve:
            raise InsufficientFundsError(f"Cannot breach minimum reserve of {self.min_reserve}")
        self._balance -= amount

    def apply_monthly_interest(self) -> float:
        accrual = self._balance * (self.interest_rate / 12.0)
        self._balance += accrual
        return accrual


class CurrentAccount(BaseAccount):
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
        self._balance -= amount
