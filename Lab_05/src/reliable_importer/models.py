from dataclasses import dataclass
from typing import Literal

Operation = Literal["deposit", "withdraw"]


@dataclass(slots=True, frozen=True)
class BankingEntry:
    account_number: str
    client: str
    balance: float
    operation: Operation
    amount: float
    final_balance: float
