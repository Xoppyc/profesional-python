from __future__ import annotations

from pathlib import Path

from application.config import load_config


def test_load_configuration_rules(tmp_path: Path) -> None:
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(
        "allowed_operations:\n"
        "  - deposit\n"
        "  - withdraw\n"
        "allowed_currencies:\n"
        "  - UAH\n"
        "  - USD\n"
        "min_balance: 100.0\n",
        encoding="utf-8",
    )

    config = load_config(yaml_file)
    assert "deposit" in config.allowed_operations
    assert "USD" in config.allowed_currencies
    assert config.min_balance == 100.0
