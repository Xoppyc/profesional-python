from __future__ import annotations

from typing import Protocol, TypeVar

T = TypeVar("T")


class Identifiable(Protocol):
    @property
    def identifier(self) -> str: ...


class Repository(Protocol[T]):
    def add(self, entity: T) -> None: ...

    def get_by_id(self, entity_id: str) -> T | None: ...

    def list_all(self) -> list[T]: ...

    def delete(self, entity_id: str) -> bool: ...


class Notifier(Protocol):
    def notify(self, message: str) -> None: ...

    def send(self, message: str) -> None: ...


NotificationService = Notifier
