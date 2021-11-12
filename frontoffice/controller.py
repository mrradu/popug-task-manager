from loguru import logger
from sqlalchemy.orm import Session

from frontoffice import models
from frontoffice.models import AccountsModel
from frontoffice.schemas import BaseAccount


def get_user(db: Session, public_id: str):
    """Получение юзера по email."""
    return (
        db.query(models.AccountsModel)
        .filter(models.AccountsModel.public_id == public_id)
        .first()
    )


def get_users(db: Session):
    return db.query(models.AccountsModel).all()


def add_account(db: Session, account: BaseAccount):
    logger.info(f"Add account: {account}")
    account = AccountsModel(
        public_id=account.public_id,
        full_name=account.full_name,
        email=account.email,
        role=account.role,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    logger.info(f"Account was added")

    return account
