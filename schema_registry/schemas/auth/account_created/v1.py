from schema_registry.schemas.base import EventParams


class AccountCreated(EventParams):
    public_id: str
    email: str
    role: str
    full_name: str
