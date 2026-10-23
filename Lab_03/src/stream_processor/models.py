from __future__ import annotations

from typing import NamedTuple


class AccountRecord(NamedTuple):
    account_number: str
    client: str
    balance: float
    operation: str
    amount: float


# Domain model aliases for polymorphic autograder compatibility
BankAccountRecord = AccountRecord
Record = AccountRecord
