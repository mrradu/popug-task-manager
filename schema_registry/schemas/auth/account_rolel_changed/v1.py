from schema_registry.schemas.base import EventParams


class AccountRoleChanged(EventParams):
    public_id: str
    role: str
