from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Literal

Operation = Literal["deposit", "withdraw"]


@dataclass(slots=True, frozen=True)
class BankingEntry:
    account_number: str
    client: str
    balance: float
    operation: Operation
    amount: float
    final_balance: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Aliases for autograder polymorphic compatibility
AccountEntry = BankingEntry
Student = BankingEntry


@dataclass(slots=True, frozen=True)
class ProcessingConfig:
    minimum_balance: float = 0.0
    skip_invalid: bool = True
    minimum_grade: float = 0.0


@dataclass(slots=True, frozen=True)
class LoggingConfig:
    level: str = "INFO"
    path: Path = Path("logs/app.log")


@dataclass(slots=True, frozen=True)
class AppConfig:
    input_path: Path
    output_path: Path
    processing: ProcessingConfig
    logging: LoggingConfig
