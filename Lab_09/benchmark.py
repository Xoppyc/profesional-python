import time

from bank_perf.analytics import (
    calculate_total_multiprocess,
    calculate_total_numpy,
    calculate_total_sequential,
    get_cached_account_metrics,
)
from bank_perf.dataset import generate_synthetic_accounts


def run_benchmark() -> None:
    print("Generating 100,000 synthetic banking accounts...")
    dataset = generate_synthetic_accounts(100_000)

    # 1. Sequential
    t0 = time.perf_counter()
    res_seq = calculate_total_sequential(dataset)
    t_seq = time.perf_counter() - t0
    print(f"Sequential: {t_seq * 1000:.2f} ms (Total: {res_seq:.2f})")

    # 2. NumPy
    t0 = time.perf_counter()
    res_np = calculate_total_numpy(dataset)
    t_np = time.perf_counter() - t0
    print(f"NumPy: {t_np * 1000:.2f} ms (Total: {res_np:.2f})")

    # 3. Multiprocessing
    t0 = time.perf_counter()
    res_mp = calculate_total_multiprocess(dataset, workers=2)
    t_mp = time.perf_counter() - t0
    print(f"ProcessPool: {t_mp * 1000:.2f} ms (Total: {res_mp:.2f})")

    # 4. Cache
    metrics = get_cached_account_metrics(hash(100_000), len(dataset), res_seq)
    print(f"Cached metrics: {metrics}")


if __name__ == "__main__":
    run_benchmark()
