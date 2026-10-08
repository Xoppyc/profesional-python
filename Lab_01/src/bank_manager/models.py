from dataclasses import dataclass


@dataclass(slots=True)
class Account:
    account_number: str
    client_name: str
    balance: float

    def __post_init__(self) -> None:
        if self.balance < 0:
            # Enforce non-negative ledger balance to maintain double-entry integrity
            raise ValueError(f"Account balance cannot be negative: {self.balance}")
