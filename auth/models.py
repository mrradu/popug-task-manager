import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    sql,
)

from auth.db import Base
from auth.enums import UserRole


def generate_uuid():
    return str(uuid.uuid4())


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String, default=generate_uuid)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class UserTokenModel(Base):
    __tablename__ = "users_token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=sql.func.current_timestamp()
    )
    updated_at = Column(TIMESTAMP, nullable=True)
