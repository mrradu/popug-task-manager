from abc import ABC, abstractmethod

from inventory.events.base import Event


class BaseEventPerformer(ABC):
    """Базовый исполнитель события."""

    event_name: str

    @classmethod
    def matches(self, event: Event) -> bool:
        """Матчим исполнителя по названию события."""
        return event.event_name == self.event_name

    @abstractmethod
    def execute(self, event: Event):
        """Исполняем логику для события."""
        pass
