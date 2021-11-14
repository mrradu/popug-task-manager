from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from inventory.enums import ItemsStatus, UserRole


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


class TaskBase(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    account_id: Optional[int]
    public_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    status: ItemsStatus


class Tasks(BaseModel):
    tasks: List[Task]

    class Config:
        orm_mode = True


class AccountUpdateFields(BaseModel):
    public_id: str
    role: Optional[UserRole]
    full_name: Optional[str]

    class Config:
        use_enum_values = True
