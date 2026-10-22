from dataclasses import dataclass
from pathlib import Path

import yaml

from reliable_importer.exceptions import ConfigurationError


@dataclass(slots=True, frozen=True)
class ImporterConfig:
    strict_mode: bool
    min_balance: float
    max_single_transfer: float
    allowed_operations: set[str]
    input_csv: Path
    output_json: Path
    log_file: Path


def load_config(config_path: Path) -> ImporterConfig:
    if not config_path.exists():
        raise ConfigurationError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return ImporterConfig(
        strict_mode=data["app"]["strict_mode"],
        min_balance=float(data["validation"]["min_balance"]),
        max_single_transfer=float(data["validation"]["max_single_transfer"]),
        allowed_operations=set(data["validation"]["allowed_operations"]),
        input_csv=Path(data["paths"]["input_csv"]),
        output_json=Path(data["paths"]["output_json"]),
        log_file=Path(data["paths"]["log_file"]),
    )
