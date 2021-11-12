from pydantic import BaseModel

from frontoffice.enums import UserRole


class BaseAccount(BaseModel):
    public_id: str
    full_name: str
    email: str
    role: UserRole

    class Config:
        orm_mode = True
