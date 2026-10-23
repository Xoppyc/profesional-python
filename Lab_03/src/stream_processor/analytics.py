from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from stream_processor.models import AccountRecord


def calculate_total_balance(accounts: Iterable[AccountRecord]) -> float:
    # Accumulate running total via O(1) space traversal
    return sum(acc.balance for acc in accounts)


def calculate_statistics(accounts: Iterable[AccountRecord]) -> dict[str, Any]:
    count = 0
    total = 0.0
    minimum: float | None = None
    maximum: float | None = None

    for acc in accounts:
        count += 1
        total += acc.balance
        if minimum is None or acc.balance < minimum:
            minimum = acc.balance
        if maximum is None or acc.balance > maximum:
            maximum = acc.balance

    average = (total / count) if count > 0 else 0.0

    return {
        "count": count,
        "total": round(total, 2),
        "average": round(average, 2),
        "minimum": minimum,
        "maximum": maximum,
    }


stream_total_balance = calculate_total_balance
