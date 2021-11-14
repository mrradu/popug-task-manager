from typing import Optional

from pydantic import BaseModel

from auth.enums import UserRole


class UserBase(BaseModel):
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    public_id: str
    role: UserRole
    is_active: bool
    hashed_password: str

    class Config:
        orm_mode = True


class UserUpdateFields(BaseModel):
    public_id: str
    role: Optional[UserRole]
    full_name: Optional[str]

    class Config:
        use_enum_values = True
