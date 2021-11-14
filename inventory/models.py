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

from inventory.db import Base
from inventory.enums import ItemsStatus, UserRole


def generate_uuid():
    return str(uuid.uuid4())


class ItemsModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    public_id = Column(String, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Enum(ItemsStatus), nullable=False, default=ItemsStatus.FREE)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=sql.func.current_timestamp()
    )
    updated_at = Column(TIMESTAMP, nullable=True)


class AccountsModel(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False, default=UserRole.EMPLOYEE.value)
    is_active = Column(Boolean, default=True)


class AuthIdentities(Base):
    __tablename__ = "auth_identities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    token = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=sql.func.current_timestamp()
    )
    updated_at = Column(TIMESTAMP, nullable=True)


# class ItemsStatusesModel(Base):
#     __tablename__ = "items_statuses"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     # account_id = Column(Integer, ForeignKey("accounts.id"))
#     item_id = Column(Integer, ForeignKey("items.id"))
#     status = Column(Enum(ItemsStatus), nullable=False, default=ItemsStatus.FREE)
#
#     item = relationship("ItemsModel", back_populates="items_statuses")
