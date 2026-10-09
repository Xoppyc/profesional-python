import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def measure_execution_time(func: F) -> F:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        print(f"[BENCHMARK] {func.__name__} executed in {elapsed_ms:.4f} ms")
        return result

    return wrapper  # type: ignore[return-value]


def audit_transaction_call(action_name: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"[AUDIT] Starting action '{action_name}'...")
            res = func(*args, **kwargs)
            print(f"[AUDIT] Finished action '{action_name}' successfully.")
            return res

        return wrapper  # type: ignore[return-value]

    return decorator
