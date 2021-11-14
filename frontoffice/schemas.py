from typing import Optional

from pydantic import BaseModel

from frontoffice.enums import UserRole


class BaseAccount(BaseModel):
    public_id: str
    full_name: str
    email: str
    role: UserRole

    class Config:
        orm_mode = True
        use_enum_values = True


class Account(BaseAccount):
    id: int
    is_active: bool


class AccountUpdateFields(BaseModel):
    public_id: str
    role: Optional[UserRole]
    full_name: Optional[str]

    class Config:
        use_enum_values = True
