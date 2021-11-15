import importlib
import re
from enum import Enum
from typing import Any, Dict

from loguru import logger
from pydantic import ValidationError

from schema_registry.schemas.base import Event, EventMeta, EventParamsT


class SchemaRegistry:
    """Реестр схем"""

    def __init__(self):
        self.schemas_path = "schema_registry.schemas"

    def _get_event_dir(self, event_name: str):
        return "_".join(re.findall("[A-Z][^A-Z]*", event_name)).lower()

    def _get_params_class(self, event_meta: EventMeta) -> EventParamsT:
        event_dir = self._get_event_dir(event_meta.event_name)
        event_path = importlib.import_module(
            f"{self.schemas_path}."
            f"{event_meta.event_producer}."
            f"{event_dir}."
            f"{event_meta.event_version}"
        )
        return getattr(event_path, event_meta.event_name)

    def validate(self, event: Dict[str, Any]):
        try:
            event_meta = EventMeta(**event)
            params_class = self._get_params_class(event_meta)
            return bool(Event[params_class](**event))
        except ValidationError as exc:
            logger.error(f"Event validation error. Error: \n {exc.json()}")
            return None


schema_registry = SchemaRegistry()
