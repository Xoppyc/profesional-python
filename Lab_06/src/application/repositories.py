from __future__ import annotations

from typing import Any, Protocol, TypeVar

from application.models import Account

T = TypeVar("T")


class Repository(Protocol[T]):
    def add(self, entity: T) -> None: ...
    def get_by_id(self, entity_id: str) -> T | None: ...
    def list_all(self) -> list[T]: ...
    def delete(self, entity_id: str) -> bool: ...


class FakeRepository:
    def __init__(self) -> None:
        self.items: dict[str, Any] = {}

    def add(self, item: Any) -> None:
        key = getattr(item, "account_number", getattr(item, "identifier", str(id(item))))
        self.items[key] = item

    def get_by_id(self, entity_id: str) -> Any | None:
        return self.items.get(entity_id)

    def list_all(self) -> list[Any]:
        return list(self.items.values())

    def delete(self, entity_id: str) -> bool:
        return self.items.pop(entity_id, None) is not None


class InMemoryAccountRepository:
    def __init__(self) -> None:
        self._items: dict[str, Account] = {}

    def add(self, entity: Account) -> None:
        self._items[entity.account_number] = entity

    def get_by_id(self, entity_id: str) -> Account | None:
        return self._items.get(entity_id)

    def list_all(self) -> list[Account]:
        return list(self._items.values())

    def delete(self, entity_id: str) -> bool:
        return self._items.pop(entity_id, None) is not None

    def find_by_account_number(self, account_number: str) -> Account | None:
        return self.get_by_id(account_number)

    def calculate_total_funds(self) -> float:
        return round(sum(acc.balance for acc in self.list_all()), 2)


AccountRepository = InMemoryAccountRepository
