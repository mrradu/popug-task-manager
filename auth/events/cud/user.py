from loguru import logger

from auth.events.producer import Producer
from auth.schemas import User
from schema_registry.registry import schema_registry

"""
########
События.
########

event_name: 
     Название события. Должно соответствовать названию 
     директории в schemas_registry. 
     Например названия события:  AccountRoleChanged
     Название директории:        account_role_changed   

event_producer: 
    Сервис, которое отправляет событие. Является родительской
    директорией для события. 
    Например, если сервис auth, а событие AccountRoleChanged, 
    то получим структуру:

     schema_registry/
            ├── schemas/
            |    ├── auth/
            |    |   └── account_role_changed/
            |    |   |      └── v1.py/
            |    |   |      └── v2.py/

event_version:
    Версия шаблона события в формате "vN", где N номер версии.

params:
    Параметры события.
# Шаблон события:

event = {
        "event_name": "AccountRoleChanged", 
        "event_producer": "auth",
        "event_version": "v1",
        "params": {
            "public_id": user.public_id,
            "role": user.role,
        },
    }
"""


def send_create_user_event(user: User):
    """Отправка CUD события о том, что был создан новый юзер."""
    event = {
        "event_name": "AccountCreated",
        "event_producer": "auth",
        "event_version": "v1",
        "params": {
            "public_id": user.public_id,
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
        },
    }

    if schema_registry.validate(event):
        Producer().call(event, "accounts-stream")
    else:
        logger.error(f"Event error. Event data: {event}")


def send_update_user_event(user):
    """Отправка CUD события, о том, что у юзера обновились данные."""
    event = {
        "event_name": "AccountUpdated",
        "event_producer": "auth",
        "event_version": "v1",
        "params": {
            "public_id": user.public_id,
            "email": user.email,
            "full_name": user.full_name,
        },
    }
    if schema_registry.validate(event):
        Producer().call(event, "accounts-stream")
    else:
        logger.error(f"Event error. Event data: {event}")
