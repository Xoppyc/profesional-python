from __future__ import annotations

import time

from bank_perf.analytics import (
    calculate_total_numpy,
    calculate_total_sequential,
    get_cached_account_metrics,
    statistics_numpy,
    statistics_python,
)
from bank_perf.concurrency import ThreadSafeAccount
from bank_perf.dataset import generate_synthetic_accounts
from bank_perf.parallel import calculate_total_multiprocess
from bank_perf.profiling import memory_test


def main() -> None:
    print("=== Лабораторна робота №9: Паралельність, багатопроцесність та оптимізація ===")
    print("Генерація 100 000 синтетичних банківських рахунків...")
    dataset = generate_synthetic_accounts(100_000)

    t0 = time.perf_counter()
    seq_total = calculate_total_sequential(dataset)
    t_seq = time.perf_counter() - t0
    print(f"Послідовний підсумок: {t_seq * 1000:.2f} ms | Сума: {seq_total:.2f}")

    t0 = time.perf_counter()
    np_total = calculate_total_numpy(dataset)
    t_np = time.perf_counter() - t0
    print(f"NumPy векторизація: {t_np * 1000:.2f} ms | Сума: {np_total:.2f} | Speedup: {t_seq / t_np:.2f}x")

    t0 = time.perf_counter()
    mp_total = calculate_total_multiprocess(dataset, workers=2)
    t_mp = time.perf_counter() - t0
    print(f"ProcessPoolExecutor (2 workers): {t_mp * 1000:.2f} ms | Сума: {mp_total:.2f}")

    balances = [acc.balance for acc in dataset[:1000]]
    stats_py = statistics_python(balances)
    stats_np = statistics_numpy(balances)
    print(f"Статистика Python: {stats_py}")
    print(f"Статистика NumPy:  {stats_np}")

    cached = get_cached_account_metrics(hash(100_000), len(dataset), seq_total)
    print(f"Кешовані метрики: {cached}")

    acc = ThreadSafeAccount()
    acc.deposit(1000.0)
    print(f"ThreadSafeAccount баланс: {acc.balance}")

    _curr_mem, peak_mem = memory_test(10_000)
    print(f"Tracemalloc memory peak: {peak_mem / 1024:.2f} KB")


if __name__ == "__main__":
    main()
