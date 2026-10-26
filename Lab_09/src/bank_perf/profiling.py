from __future__ import annotations

import cProfile
import io
import pstats
import tracemalloc

from bank_perf.analytics import calculate_total_numpy, calculate_total_sequential
from bank_perf.dataset import generate_synthetic_accounts


def run_profile(count: int = 10_000) -> str:
    dataset = generate_synthetic_accounts(count)
    profiler = cProfile.Profile()
    profiler.enable()
    _ = calculate_total_sequential(dataset)
    _ = calculate_total_numpy(dataset)
    profiler.disable()

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream).sort_stats(pstats.SortKey.CUMULATIVE)
    stats.print_stats(15)
    return stream.getvalue()


def memory_test(count: int = 10_000) -> tuple[int, int]:
    tracemalloc.start()
    dataset = generate_synthetic_accounts(count)
    _ = calculate_total_numpy(dataset)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current, peak
