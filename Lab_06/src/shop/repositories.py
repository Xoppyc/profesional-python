from __future__ import annotations

from typing import Protocol

from shop.models import Product


class ProductRepository(Protocol):
    def get_by_id(self, product_id: int) -> Product | None: ...
    def save(self, product: Product) -> None: ...


class InMemoryProductRepository:
    def __init__(self) -> None:
        self._products: dict[int, Product] = {}

    def get_by_id(self, product_id: int) -> Product | None:
        return self._products.get(product_id)

    def save(self, product: Product) -> None:
        self._products[product.product_id] = product
