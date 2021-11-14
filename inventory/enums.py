from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class ItemsStatus(Enum):
    LOCK = "lock"
    FREE = "free"
    FINISHED = "finished"
