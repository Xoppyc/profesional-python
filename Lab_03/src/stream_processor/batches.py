from __future__ import annotations

import itertools
from collections.abc import Iterable, Iterator


def batched_accounts[T](items: Iterable[T], batch_size: int) -> Iterator[list[T]]:
    # Chunk stream into bounded windows to cap working memory during bulk ingestion
    iterator = iter(items)
    while True:
        chunk = list(itertools.islice(iterator, batch_size))
        if not chunk:
            break
        yield chunk


def take_first_n[T](items: Iterable[T], n: int) -> Iterator[T]:
    # Truncate stream lazily via islice without evaluating remaining elements
    return itertools.islice(items, n)


batch_stream = batched_accounts
first_n = take_first_n
