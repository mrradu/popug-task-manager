from fastapi import Depends
from sqlalchemy.orm import Session

from inventory.consumer_handler.base import BaseEventPerformer
from inventory.consumer_handler.handler import event_handler
from inventory.controller import add_account
from inventory.db import get_db
from inventory.events.base import Event
from inventory.schemas import BaseAccount


@event_handler.register
class AccountCreatedEventPerformer(BaseEventPerformer):
    """Исполнитель события о регистрации юзера."""

    event_name: str = "AccountCreated"

    def execute(self, event: Event):
        """Добавление зарегистрированного юзера в БД инвентори."""
        account = BaseAccount(**event.data)
        db = get_db()
        add_account(db=next(db), account=account)
