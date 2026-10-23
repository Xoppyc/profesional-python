from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Money:
    amount: float
    currency: str = "UAH"


@dataclass(slots=True, frozen=True)
class AccountNumber:
    value: str


@dataclass(slots=True, frozen=True)
class TransactionId:
    value: str
