from __future__ import annotations

import logging
from pathlib import Path

from reliable_importer.config import load_config
from reliable_importer.exceptions import ApplicationError
from reliable_importer.exporters import export_accounts_json
from reliable_importer.logging_config import setup_logging
from reliable_importer.services import ImportStatistics, filter_by_balance, import_accounts
from reliable_importer.utils import logged_operation

logger = logging.getLogger(__name__)


def main() -> None:
    base_dir = Path(__file__).resolve().parent.parent.parent
    config_file = base_dir / "config.yaml"
    if not config_file.exists():
        config_file = Path("config.yaml")

    try:
        config = load_config(config_file)
        setup_logging(config.logging.path)

        with logged_operation("Full batch import pipeline"):
            stats = ImportStatistics()
            input_file = (
                base_dir / config.input_path
                if not config.input_path.is_absolute()
                else config.input_path
            )
            output_file = (
                base_dir / config.output_path
                if not config.output_path.is_absolute()
                else config.output_path
            )

            accounts = import_accounts(
                input_file,
                skip_invalid=config.processing.skip_invalid,
                statistics=stats,
                min_balance=config.processing.minimum_balance,
            )
            filtered = filter_by_balance(accounts, config.processing.minimum_balance)
            exported_count = export_accounts_json(filtered, output_file)

            print(
                f"Import summary: total={stats.total}, valid={stats.valid}, "
                f"invalid={stats.invalid}, exported={exported_count}"
            )
    except ApplicationError as err:
        logger.critical("Application failed with domain error: %s", err)
        raise SystemExit(1) from err


if __name__ == "__main__":
    main()
