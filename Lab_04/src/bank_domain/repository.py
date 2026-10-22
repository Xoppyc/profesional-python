from bank_domain.protocols import Identifiable


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
        if entity_id in self._storage:
            del self._storage[entity_id]
            return True
        return False
