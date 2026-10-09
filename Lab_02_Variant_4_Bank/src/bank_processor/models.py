from dataclasses import dataclass
from typing import Literal

AccountType = Literal["checking", "savings", "deposit", "credit"]


@dataclass(slots=True, frozen=True)
class AccountRecord:
    account_number: str
    client_name: str
    balance: float
    account_type: AccountType

    def __post_init__(self) -> None:
        if self.balance < 0:
            raise ValueError(f"Balance must be non-negative: {self.balance}")
