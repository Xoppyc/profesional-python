from __future__ import annotations

from typing import TypeVar

from domain_app.models import Account
from domain_app.protocols import Identifiable

T = TypeVar("T", bound=Identifiable)


class InMemoryRepository[T: Identifiable]:
    def __init__(self) -> None:
        self._storage: dict[str, T] = {}

    def add(self, entity: T) -> None:
        self._storage[entity.identifier] = entity

    def get_by_id(self, entity_id: str) -> T | None:
        return self._storage.get(entity_id)

    def list_all(self) -> list[T]:
        return list(self._storage.values())

    def delete(self, entity_id: str) -> bool:
        return self._storage.pop(entity_id, None) is not None


class AccountRepository(InMemoryRepository[Account]):
    def find_by_account_number(self, account_number: str) -> Account | None:
        return self.get_by_id(account_number)

    def calculate_total_funds(self) -> float:
        return round(sum(acc.balance for acc in self.list_all()), 2)
