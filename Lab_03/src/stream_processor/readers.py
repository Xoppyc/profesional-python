from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def read_lines(path: Path | str) -> Iterator[str]:
    # Stream lines lazily to maintain constant memory consumption irrespective of stream scale
    with Path(path).open("r", encoding="utf-8") as file:
        yield from file
