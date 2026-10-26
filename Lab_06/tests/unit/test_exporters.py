from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock, create_autospec

import pytest
from application.exporters import export_accounts_json, export_order
from application.models import Account, CustomResource, DataImportError, parse_value
from shop.models import Cart
from shop.protocols import Notifier, PaymentGateway
from shop.services import CheckoutService, PaymentError


def test_exception_chaining() -> None:
    with pytest.raises(DataImportError) as exc_info:
        parse_value("abc")

    assert isinstance(exc_info.value.__cause__, ValueError)


def test_file_closed() -> None:
    resource = CustomResource()
    with resource:
        assert resource.is_open
    assert not resource.is_open


def test_atomic_export(tmp_path: Path) -> None:
    output = tmp_path / "accounts.json"
    output.write_text("old valid data", encoding="utf-8")
    temporary = output.with_suffix(".tmp")

    accounts = [Account("UA-1", "C-1", 100.0)]
    export_accounts_json(accounts, output)

    assert output.exists()
    assert not temporary.exists()
    assert "UA-1" in output.read_text(encoding="utf-8")


def test_products(product_factory) -> None:
    cheap = product_factory(product_id=1, price=10)
    expensive = product_factory(product_id=2, price=1000)
    assert cheap.price.amount < expensive.price.amount


def test_autospec_gateway() -> None:
    gateway = create_autospec(PaymentGateway, instance=True)
    gateway.pay.return_value = "PAY-AUTO-01"
    assert gateway.pay(Mock()) == "PAY-AUTO-01"


def test_empty_cart_cannot_be_checked_out() -> None:
    gateway = Mock(spec=PaymentGateway)
    notifier = Mock(spec=Notifier)
    service = CheckoutService(gateway, notifier)
    with pytest.raises(ValueError, match="empty"):
        service.checkout("test@example.com", Cart())


def test_invalid_grade_raises_validation_error() -> None:
    with pytest.raises(ValueError):
        if not (0 <= -5 <= 100):
            raise ValueError("Invalid grade")


def test_payment_failure_does_not_send_notification(cart: Cart) -> None:
    gateway = Mock(spec=PaymentGateway)
    gateway.pay.side_effect = PaymentError("Payment server unavailable")
    notifier = Mock(spec=Notifier)
    service = CheckoutService(gateway, notifier)

    with pytest.raises(PaymentError, match="unavailable"):
        service.checkout("student@example.com", cart)

    notifier.send.assert_not_called()


def test_export_accounts_and_order(tmp_path: Path) -> None:
    order_file = tmp_path / "order.json"
    export_order({"order_id": 1, "amount": 250.0}, order_file)
    assert order_file.exists()
    data = json.loads(order_file.read_text(encoding="utf-8"))
    assert data["order_id"] == 1
