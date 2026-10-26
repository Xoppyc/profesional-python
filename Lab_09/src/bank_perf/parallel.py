from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path

from bank_perf.dataset import AccountData


def _score_single_item(value: float) -> float:
    return round(value * 1.05 + 2.5, 4)


def _chunk_sum(chunk: list[AccountData]) -> float:
    return sum(acc.balance for acc in chunk)


def calculate_scores_processes(values: list[float], workers: int = 2) -> list[float]:
    if not values:
        return []
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_score_single_item, values))


def calculate_scores_threads(values: list[float], workers: int = 2) -> list[float]:
    if not values:
        return []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_score_single_item, values))


def calculate_total_multiprocess(accounts: list[AccountData], workers: int = 2) -> float:
    if not accounts:
        return 0.0
    chunk_size = max(1, len(accounts) // workers)
    chunks = [accounts[i : i + chunk_size] for i in range(0, len(accounts), chunk_size)]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = executor.map(_chunk_sum, chunks)
    return sum(results)


def load_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def load_files_parallel(paths: list[str], workers: int = 4) -> list[str]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(load_file, paths))
