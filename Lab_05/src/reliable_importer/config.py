from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from reliable_importer.exceptions import ConfigurationError
from reliable_importer.models import AppConfig, LoggingConfig, ProcessingConfig


@dataclass(slots=True, frozen=True)
class ImporterConfig:
    strict_mode: bool
    min_balance: float
    max_single_transfer: float
    allowed_operations: set[str]
    input_csv: Path
    output_json: Path
    log_file: Path


def load_config(config_path: Path | str) -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        raise ConfigurationError(f"Config file not found: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = yaml.safe_load(f) or {}
    except Exception as exc:
        raise ConfigurationError(f"Failed to parse YAML config: {exc}") from exc

    # Parse paths
    paths_data = data.get("paths", {})
    input_str = paths_data.get("input_path") or paths_data.get("input_csv") or "data/accounts.csv"
    output_str = (
        paths_data.get("output_path")
        or paths_data.get("output_json")
        or "output/accounts_export.json"
    )

    # Parse processing
    proc_data = data.get("processing", {})
    min_bal = float(
        proc_data.get("minimum_balance", data.get("validation", {}).get("min_balance", 0.0))
    )
    skip_inv = bool(
        proc_data.get("skip_invalid", not data.get("app", {}).get("strict_mode", False))
    )

    processing = ProcessingConfig(
        minimum_balance=min_bal,
        skip_invalid=skip_inv,
        minimum_grade=min_bal,
    )

    # Parse logging
    log_data = data.get("logging", {})
    log_level = str(log_data.get("level", "INFO"))
    log_path_str = log_data.get("path") or paths_data.get("log_file") or "logs/importer.log"
    logging_cfg = LoggingConfig(level=log_level, path=Path(log_path_str))

    return AppConfig(
        input_path=Path(input_str),
        output_path=Path(output_str),
        processing=processing,
        logging=logging_cfg,
    )
