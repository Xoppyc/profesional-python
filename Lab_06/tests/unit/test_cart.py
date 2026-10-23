from __future__ import annotations

import pytest
from shop.models import Cart, Product


def test_empty_cart() -> None:
    cart = Cart()
    assert len(cart) == 0
    assert cart.total.amount == 0


def test_cart_length(cart: Cart) -> None:
    assert len(cart) == 2


def test_cart_contains_product(cart: Cart) -> None:
    assert 1 in cart
    assert 2 in cart
    assert 999 not in cart


def test_cart_total(cart: Cart) -> None:
    assert cart.total.amount == pytest.approx(37_400)


@pytest.mark.parametrize("quantity", [0, -1, -100])
def test_invalid_quantity(laptop: Product, quantity: int) -> None:
    cart = Cart()
    with pytest.raises(ValueError, match="positive"):
        cart.add(laptop, quantity)
