from __future__ import annotations

import pytest
from bank_perf.analytics import (
    calculate_total_numpy,
    calculate_total_sequential,
    get_cached_account_metrics,
)
from bank_perf.concurrency import ThreadSafeAccount
from bank_perf.dataset import AccountData
from bank_perf.parallel import calculate_total_multiprocess
from bank_perf.profiling import memory_test, run_profile


def test_calculations_equality() -> None:
    data = [AccountData("A1", 100.0), AccountData("A2", 250.5), AccountData("A3", 49.5)]
    seq = calculate_total_sequential(data)
    np_res = calculate_total_numpy(data)
    assert seq == 400.0
    assert round(np_res, 2) == 400.0


def test_multiprocess_total() -> None:
    data = [AccountData(f"A{i}", float(i * 10)) for i in range(1, 21)]
    seq = calculate_total_sequential(data)
    mp_res = calculate_total_multiprocess(data, workers=2)
    assert mp_res == pytest.approx(seq)


def test_thread_safe_account() -> None:
    acc = ThreadSafeAccount(0.0)
    acc.deposit(50.0)
    acc.deposit(150.0)
    assert acc.balance == 200.0


def test_cached_account_metrics() -> None:
    metrics1 = get_cached_account_metrics(12345, 10, 1000.0)
    metrics2 = get_cached_account_metrics(12345, 10, 1000.0)
    assert metrics1 == metrics2
    assert metrics1["average"] == 100.0


def test_profiling_and_memory() -> None:
    output = run_profile(count=100)
    assert "function calls" in output
    _, peak = memory_test(count=100)
    assert peak > 0
