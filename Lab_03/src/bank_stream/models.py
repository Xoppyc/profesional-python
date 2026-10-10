from dataclasses import dataclass
from typing import Literal

OperationType = Literal["deposit", "withdraw", "transfer"]


@dataclass(slots=True, frozen=True)
class StreamTransaction:
    transaction_id: str
    account_number: str
    client_name: str
    operation: OperationType
    amount: float
    current_balance: float
