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


class Account(BaseAccount):
    id: int


class TaskBase(BaseModel):
    account_id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    public_id: str
    created_at: datetime
    updated_at: Optional[datetime]
    status: ItemsStatus


class Tasks(BaseModel):
    tasks: List[Task]

    class Config:
        orm_mode = True
