from enum import Enum


class UserRole(Enum):
    ADMIN: str = "admin"
    MANAGER: str = "manager"
    EMPLOYEE: str = "employee"


class ItemsStatus(Enum):
    LOCK: str = "lock"
    FREE: str = "free"
    FINISHED: str = "finished"
