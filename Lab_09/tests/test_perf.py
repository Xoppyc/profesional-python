from bank_perf.analytics import calculate_total_numpy, calculate_total_sequential
from bank_perf.concurrency import ThreadSafeAccount
from bank_perf.dataset import AccountData


def test_calculations_equality() -> None:
    data = [AccountData("A1", 100.0), AccountData("A2", 250.5), AccountData("A3", 49.5)]
    seq = calculate_total_sequential(data)
    np_res = calculate_total_numpy(data)
    assert seq == 400.0
    assert round(np_res, 2) == 400.0


def test_thread_safe_account() -> None:
    acc = ThreadSafeAccount(0.0)
    acc.deposit(50.0)
    acc.deposit(150.0)
    assert acc.balance == 200.0
