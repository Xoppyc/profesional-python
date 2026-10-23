from __future__ import annotations

from typing import TypedDict


class CustomerDTO(TypedDict):
    customer_id: str
    full_name: str
    email: str


class AccountDTO(TypedDict):
    account_number: str
    customer_id: str
    balance: float
    account_type: str


class TransactionDTO(TypedDict):
    transaction_id: str
    account_number: str
    amount: float
    operation_type: str
    timestamp: str
