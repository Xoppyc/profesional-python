from __future__ import annotations

from pathlib import Path

import pytest
from application.config import AppConfig, get_payment_mode, load_config


@pytest.mark.integration
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


@pytest.mark.integration
def test_default_config_fallback() -> None:
    config = load_config("non_existing_file.yaml")
    assert isinstance(config, AppConfig)
    assert "deposit" in config.allowed_operations
    assert "UAH" in config.allowed_currencies


@pytest.mark.integration
def test_payment_mode_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PAYMENT_MODE", "test")
    assert get_payment_mode() == "test"


@pytest.mark.integration
def test_default_payment_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("PAYMENT_MODE", raising=False)
    assert get_payment_mode() == "sandbox"
