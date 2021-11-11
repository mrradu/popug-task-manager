from typing import Any, Dict

from pydantic import BaseModel


class Event(BaseModel):
    """Объект события."""

    event_name: str
    data: Dict[str, Any]
