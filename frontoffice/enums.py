from enum import Enum


class UserRole(Enum):
    ADMIN: str = "admin"
    MANAGER: str = "manager"
    EMPLOYEE: str = "employee"
