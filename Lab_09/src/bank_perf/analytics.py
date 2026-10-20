from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
import numpy as np
from bank_perf.dataset import AccountData


def calculate_total_sequential(accounts: list[AccountData]) -> float:
    total = 0.0
    for acc in accounts:
        total += acc.balance
    return total


def calculate_total_numpy(accounts: list[AccountData]) -> float:
    # Vectorized computation leveraging SIMD CPU instructions
    balances = np.array([acc.balance for acc in accounts], dtype=np.float64)
    return float(np.sum(balances))


def _chunk_sum(chunk: list[AccountData]) -> float:
    return sum(acc.balance for acc in chunk)


def calculate_total_multiprocess(accounts: list[AccountData], workers: int = 4) -> float:
    chunk_size = len(accounts) // workers
    chunks = [accounts[i : i + chunk_size] for i in range(0, len(accounts), chunk_size)]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(_chunk_sum, chunks)
    return sum(results)


@lru_cache(maxsize=128)
def get_cached_account_metrics(dataset_hash: int, total_count: int, total_sum: float) -> dict[str, float]:
    return {
        "count": float(total_count),
        "total_funds": total_sum,
        "average": total_sum / total_count if total_count > 0 else 0.0,
    }
