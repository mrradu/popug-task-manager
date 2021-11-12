from frontoffice.consumer_handler.base import BaseEventPerformer, Event
from frontoffice.consumer_handler.handler import event_handler
from frontoffice.controller import add_account
from frontoffice.db import get_db
from frontoffice.schemas import BaseAccount


@event_handler.register
class AccountCreatedEventPerformer(BaseEventPerformer):
    """Исполнитель события о регистрации юзера."""

    event_name: str = "AccountCreated"

    def execute(self, event: Event):
        """Добавление зарегистрированного юзера в БД инвентори."""
        account = BaseAccount(**event.data)
        db = get_db()
        add_account(db=next(db), account=account)
