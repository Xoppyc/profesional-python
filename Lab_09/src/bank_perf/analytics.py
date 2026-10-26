from __future__ import annotations

from functools import lru_cache

import numpy as np

from bank_perf.dataset import AccountData


def calculate_total_sequential(accounts: list[AccountData]) -> float:
    total = 0.0
    for acc in accounts:
        total += acc.balance
    return total


def calculate_total_numpy(accounts: list[AccountData]) -> float:
    balances = np.array([acc.balance for acc in accounts], dtype=np.float64)
    return float(np.sum(balances))


def statistics_python(values: list[float]) -> dict[str, float]:
    if not values:
        return {"average": 0.0, "minimum": 0.0, "maximum": 0.0, "sum": 0.0}
    total = sum(values)
    return {
        "average": total / len(values),
        "minimum": min(values),
        "maximum": max(values),
        "sum": total,
    }


def statistics_numpy(values: list[float]) -> dict[str, float]:
    if not values:
        return {"average": 0.0, "minimum": 0.0, "maximum": 0.0, "sum": 0.0}
    arr = np.array(values, dtype=np.float64)
    return {
        "average": float(np.mean(arr)),
        "minimum": float(np.min(arr)),
        "maximum": float(np.max(arr)),
        "sum": float(np.sum(arr)),
    }


def calculate_scores_sequential(values: list[float]) -> list[float]:
    # Compute adjusted interest yields sequentially
    return [round(v * 1.05 + 2.5, 4) for v in values]


@lru_cache(maxsize=128)
def get_cached_account_metrics(
    dataset_hash: int, total_count: int, total_sum: float
) -> dict[str, float]:
    return {
        "count": float(total_count),
        "total_funds": total_sum,
        "average": total_sum / total_count if total_count > 0 else 0.0,
    }


@lru_cache(maxsize=128)
def cached_group_statistics(group_key: str, balances: tuple[float, ...]) -> dict[str, float | str]:
    if not balances:
        return {"group": group_key, "total": 0.0, "mean": 0.0}
    total = sum(balances)
    return {
        "group": group_key,
        "total": round(total, 2),
        "mean": round(total / len(balances), 2),
    }
