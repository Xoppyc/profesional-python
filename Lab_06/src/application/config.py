from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore[import-untyped]
except ImportError:
    yaml = None


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

    data: dict[str, Any] = {}
    if yaml is not None:
        with config_file.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    else:
        # Fallback simple line-based parser when pyyaml is not in environment
        current_list: list[str] | None = None
        for line in config_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("allowed_operations:"):
                current_list = []
                data["allowed_operations"] = current_list
            elif line.startswith("allowed_currencies:"):
                current_list = []
                data["allowed_currencies"] = current_list
            elif line.startswith("- ") and current_list is not None:
                current_list.append(line[2:].strip().strip("\"'"))
            elif ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip("\"'")

    ops = set(data.get("allowed_operations", ["deposit", "withdraw"]))
    currencies = set(data.get("allowed_currencies", ["UAH", "USD", "EUR"]))
    min_bal = float(data.get("min_balance", 0.0))

    return AppConfig(
        allowed_operations=ops,
        allowed_currencies=currencies,
        min_balance=min_bal,
    )
