import logging
from pathlib import Path


def mask_sensitive_account(account_number: str) -> str:
    # Mask intermediate digits to comply with banking privacy standards
    if len(account_number) <= 4:
        return "****"
    return f"{account_number[:2]}****{account_number[-2:]}"


def setup_logger(log_file: Path) -> logging.Logger:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("BankImporter")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
