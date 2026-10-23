from __future__ import annotations

import logging
from pathlib import Path

from reliable_importer.models import LoggingConfig


def mask_sensitive_account(account_number: str) -> str:
    # Mask intermediate characters to prevent leaking confidential banking records in logs
    if len(account_number) <= 4:
        return "****"
    return f"{account_number[:2]}****{account_number[-2:]}"


def setup_logger(log_target: Path | str | LoggingConfig) -> logging.Logger:
    if isinstance(log_target, LoggingConfig):
        log_file = log_target.path
        level_str = log_target.level
    else:
        log_file = Path(log_target)
        level_str = "INFO"

    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("reliable_importer")
    level = getattr(logging, level_str.upper(), logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


configure_logging = setup_logger
setup_logging = setup_logger
