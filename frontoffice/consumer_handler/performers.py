from fastapi import Depends

from frontoffice.consumer_handler.base import BaseEventPerformer, Event
from frontoffice.consumer_handler.handler import event_handler
from frontoffice.db import get_storage
from frontoffice.schemas import AccountUpdateFields, BaseAccount


@event_handler.register
class AccountCreatedEventPerformer(BaseEventPerformer):
    """Исполнитель события о регистрации юзера."""

    event_name: str = "AccountCreated"

    def execute(self, event: Event):
        """Добавление зарегистрированного юзера в БД."""
        account = BaseAccount(**event.data)
        storage = get_storage()
        storage.user.add_account(account=account)


@event_handler.register
class AccountUpdateDataEventPerformer(BaseEventPerformer):
    """Исполнитель события об обновлении данных юзера."""

    event_name: str = "AccountUpdated"

    def execute(self, event: Event):
        """Обновление данных о юзера в БД."""
        user_fields = AccountUpdateFields(**event.data)
        storage = get_storage()
        storage.user.update_user(user_fields=user_fields)


@event_handler.register
class AccountUpdateDataRoleEventPerformer(BaseEventPerformer):
    """Исполнитель события об обновлении данных юзера."""

    event_name: str = "AccountRoleChanged"

    def execute(self, event: Event):
        """Обновление данных о юзера в БД."""
        user_fields = AccountUpdateFields(**event.data)
        storage = get_storage()
        storage.user.update_user(user_fields=user_fields)
