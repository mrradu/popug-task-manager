from auth.events.producer import Producer


def send_update_user_role_event(user):
    """Отправка бизнес события о том, у юзера обновилась роль."""
    event = {
        "event_name": "AccountRoleChanged",
        "data": {
            "public_id": user.public_id,
            "role": user.role,
        },
    }
    Producer().call(event, "accounts")
