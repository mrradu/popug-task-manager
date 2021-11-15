from typing import TypeVar

from pydantic import BaseModel, Extra
from pydantic.generics import GenericModel
from pydantic.schema import Generic


class EventParams(BaseModel):
    class Config:
        extra = Extra.allow


EventParamsT = TypeVar("EventParamsT", bound=EventParams)


class EventMeta(BaseModel):
    event_name: str
    event_version: str
    event_producer: str

    class Config:
        extra = Extra.allow


class Event(EventMeta, GenericModel, Generic[EventParamsT]):
    params: EventParamsT
