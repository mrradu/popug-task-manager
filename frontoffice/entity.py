from pydantic import BaseModel


class User(BaseModel):
    email: str
    id: int
    full_name: str
    is_active: bool
    role: str
    public_id: str
