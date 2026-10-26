from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]


@dataclass(slots=True, frozen=True)
class AppConfig:
    allowed_operations: set[str] = field(default_factory=lambda: {"deposit", "withdraw"})
    allowed_currencies: set[str] = field(default_factory=lambda: {"UAH", "USD", "EUR"})
    min_balance: float = 0.0


def get_payment_mode() -> str:
    return os.getenv("PAYMENT_MODE", "sandbox")


def load_config(path: Path | str) -> AppConfig:
    config_file = Path(path)
    if not config_file.exists():
        return AppConfig()

    with config_file.open("r", encoding="utf-8") as f:
        data: dict[str, Any] = yaml.safe_load(f) or {}

    ops = set(data.get("allowed_operations", ["deposit", "withdraw"]))
    currencies = set(data.get("allowed_currencies", ["UAH", "USD", "EUR"]))
    min_bal = float(data.get("min_balance", 0.0))

    return AppConfig(
        allowed_operations=ops,
        allowed_currencies=currencies,
        min_balance=min_bal,
    )
