from typing import List, Type, TYPE_CHECKING

from loguru import logger

from inventory.events.base import Event
from inventory.consumer_handler.base import BaseEventPerformer


class EventPerformerNotFound(Exception):
    pass


class EventHandler:
    """Обработчик событий."""

    def __init__(self):
        self._registry: List[Type[BaseEventPerformer]] = []

    def register(self, klass: Type[BaseEventPerformer]):
        """Регистрация события в реестре."""
        if not issubclass(klass, BaseEventPerformer):
            raise TypeError("You can register only subclasses of BaseEventPerformer")

        self._registry.append(klass)

        return klass

    def process_event(self, event: Event):
        """Обработка события."""
        logger.info(f"Process event {event}")
        for event_performer in self._registry:
            if event_performer.matches(event):
                event_performer().execute(event)
                return

        raise EventPerformerNotFound(f"Cannot find event performer for event {event}")


event_handler = EventHandler()
