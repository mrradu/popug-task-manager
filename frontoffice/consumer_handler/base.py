from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel

from frontoffice.service import Storage


class Event(BaseModel):
    """Объект события."""

    event_name: str
    data: Dict[str, Any]


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
