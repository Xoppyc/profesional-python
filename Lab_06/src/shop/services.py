from __future__ import annotations

from shop.models import Cart
from shop.protocols import Notifier, PaymentGateway
from shop.value_objects import Money


class PaymentError(Exception):
    pass


class PercentageDiscount:
    def __init__(self, percent: float) -> None:
        if not (0 <= percent <= 100):
            raise ValueError("Invalid discount")
        self.percent = percent

    def apply(self, total: Money) -> Money:
        return Money(
            total.amount * (1 - self.percent / 100),
            total.currency,
        )


class CheckoutService:
    def __init__(self, payment_gateway: PaymentGateway, notifier: Notifier) -> None:
        self._gateway = payment_gateway
        self._notifier = notifier

    def checkout(self, email: str, cart: Cart) -> str:
        if len(cart) == 0:
            raise ValueError("Cart is empty")
        payment_id = self._gateway.pay(cart.total)
        self._notifier.send(email, f"Payment successful: {payment_id}")
        return payment_id


class AsyncPaymentStatus:
    def __init__(self, client: object) -> None:
        self._client = client

    async def get_status(self, payment_id: str) -> str:
        data = await self._client.fetch_status(payment_id)  # type: ignore[attr-defined]
        return str(data["status"])
