from auth.events.producer import Producer
from auth.schemas import User


def send_create_user_event(user: User):
    """Отправка CUD события о том, что был создан новый юзер."""
    event = {
        "event_name": "AccountCreated",
        "data": {
            "public_id": user.public_id,
            "email": user.email,
            "role": user.role.value,
            "full_name": user.full_name,
        },
    }
    Producer().call(event, "accounts-stream")


def send_update_user_event(user):
    """Отправка CUD события, о том, что у юзера обновились данные."""
    event = {
        "event_name": "AccountUpdated",
        "data": {
            "public_id": user.public_id,
            "email": user.email,
            "full_name": user.full_name,
        },
    }
    Producer().call(event, "accounts-stream")
