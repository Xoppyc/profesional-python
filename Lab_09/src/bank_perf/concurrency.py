import threading


class UnsafeSharedAccount:
    def __init__(self, initial_balance: float = 0.0) -> None:
        self.balance = initial_balance

    def deposit(self, amount: float) -> None:
        # Intentionally non-atomic read-modify-write to illustrate race conditions
        current = self.balance
        self.balance = current + amount


class ThreadSafeAccount:
    def __init__(self, initial_balance: float = 0.0) -> None:
        self.balance = initial_balance
        self._lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        with self._lock:
            # Synchronize access to shared mutable balance across threads
            current = self.balance
            self.balance = current + amount
