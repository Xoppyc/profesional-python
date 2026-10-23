from __future__ import annotations

from pathlib import Path

from stream_processor.analytics import calculate_statistics
from stream_processor.batches import take_first_n
from stream_processor.pipeline import build_pipeline


def main() -> None:
    # Resolve CSV location relative to package boundary
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_path = base_dir / "data" / "input.csv"
    if not data_path.exists():
        data_path = Path("data/input.csv")

    accounts = list(build_pipeline(data_path, minimum_balance=1000.0))
    first_three = list(take_first_n(accounts, 3))
    print(f"First 3 processed accounts: {first_three}")

    stats = calculate_statistics(accounts)
    print(f"Ledger Statistics: {stats}")


if __name__ == "__main__":
    main()
