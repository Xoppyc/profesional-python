from __future__ import annotations

import sys
from pathlib import Path

from application.config import load_config
from application.repositories import InMemoryAccountRepository
from application.services import BankingService


def main() -> int:
    config_path = Path(__file__).resolve().parent / "config.yaml"
    config = load_config(config_path)
    repo = InMemoryAccountRepository()
    service = BankingService(repo)
    print(
        "Banking application initialized with allowed operations:",
        config.allowed_operations,
        "and active service:",
        type(service).__name__,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
