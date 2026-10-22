import itertools
from collections.abc import Callable, Generator, Iterable, Iterator

from bank_stream.models import StreamTransaction


def parse_csv_stream(lines: Iterable[str]) -> Generator[StreamTransaction, None, None]:
    # Stream lines on demand to keep memory constant O(1) regardless of file size
    for line in lines:
        cleaned = line.strip()
        if not cleaned or cleaned.startswith(("#", "transaction_id")):
            continue
        parts = [p.strip() for p in cleaned.split(",")]
        if len(parts) != 6:
            continue
        try:
            yield StreamTransaction(
                transaction_id=parts[0],
                account_number=parts[1],
                client_name=parts[2],
                operation=parts[3],  # type: ignore[arg-type]
                amount=float(parts[4]),
                current_balance=float(parts[5]),
            )
        except (ValueError, TypeError):
            # Skip corrupted stream tokens
            continue


def validate_transaction_stream(
    stream: Iterable[StreamTransaction],
) -> Generator[StreamTransaction, None, None]:
    for tx in stream:
        if tx.amount > 0 and tx.current_balance >= 0:
            yield tx


def filter_by_client_stream(
    stream: Iterable[StreamTransaction],
    client_name: str,
) -> Generator[StreamTransaction, None, None]:
    target = client_name.strip().lower()
    for tx in stream:
        if tx.client_name.strip().lower() == target:
            yield tx


def filter_by_balance_threshold(
    stream: Iterable[StreamTransaction],
    min_balance: float,
) -> Generator[StreamTransaction, None, None]:
    for tx in stream:
        if tx.current_balance >= min_balance:
            yield tx


def find_first_matching(
    stream: Iterable[StreamTransaction],
    predicate: Callable[[StreamTransaction], bool],
) -> StreamTransaction | None:
    for tx in stream:
        if predicate(tx):
            return tx
    return None


def stream_total_balance(stream: Iterable[StreamTransaction]) -> float:
    return sum(tx.current_balance for tx in stream)


def take_first_n[T](stream: Iterable[T], n: int) -> Iterator[T]:
    return itertools.islice(stream, n)


def batch_stream[T](stream: Iterable[T], batch_size: int) -> Generator[list[T], None, None]:
    iterator = iter(stream)
    while True:
        chunk = list(itertools.islice(iterator, batch_size))
        if not chunk:
            break
        yield chunk
