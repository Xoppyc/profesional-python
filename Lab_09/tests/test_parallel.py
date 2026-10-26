from __future__ import annotations

import pytest
from bank_perf.analytics import (
    calculate_scores_sequential,
    statistics_numpy,
    statistics_python,
)
from bank_perf.parallel import (
    calculate_scores_processes,
    calculate_scores_threads,
    load_files_parallel,
)


def test_numpy_statistics() -> None:
    values = [
        70.0,
        80.0,
        90.0,
        100.0,
    ]
    python_result = statistics_python(values)
    numpy_result = statistics_numpy(values)

    assert numpy_result["average"] == pytest.approx(python_result["average"])
    assert numpy_result["minimum"] == pytest.approx(python_result["minimum"])
    assert numpy_result["maximum"] == pytest.approx(python_result["maximum"])


def test_process_results() -> None:
    values = [
        70.0,
        80.0,
        90.0,
    ]
    sequential = calculate_scores_sequential(values)
    parallel = calculate_scores_processes(values, workers=2)
    assert parallel == sequential


def test_thread_results() -> None:
    values = [50.0, 120.0, 300.0]
    sequential = calculate_scores_sequential(values)
    threaded = calculate_scores_threads(values, workers=2)
    assert threaded == sequential


def test_parallel_file_loading(tmp_path: pytest.TempPathFactory) -> None:
    f1 = tmp_path / "f1.txt"
    f2 = tmp_path / "f2.txt"
    f1.write_text("balance_1", encoding="utf-8")
    f2.write_text("balance_2", encoding="utf-8")
    contents = load_files_parallel([str(f1), str(f2)], workers=2)
    assert contents == ["balance_1", "balance_2"]
