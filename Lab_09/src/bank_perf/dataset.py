import random
from typing import NamedTuple


class AccountData(NamedTuple):
    account_number: str
    balance: float


def generate_synthetic_accounts(count: int = 100_000, seed: int = 42) -> list[AccountData]:
    random.seed(seed)
    return [
        AccountData(
            account_number=f"UA{i:07d}",
            balance=round(random.uniform(10.0, 50_000.0), 2),
        )
        for i in range(count)
    ]
