import time

from bank_account_service.models import Account


def run_benchmark() -> None:
    start = time.perf_counter()
    accounts = [Account(account_number=f"UA{i}", balance=float(i)) for i in range(10_000)]
    total = sum(acc.balance for acc in accounts)
    elapsed = time.perf_counter() - start
    print(f"Aggregated {len(accounts)} accounts: Total={total:.2f} in {elapsed * 1000:.2f} ms")


if __name__ == "__main__":
    run_benchmark()
