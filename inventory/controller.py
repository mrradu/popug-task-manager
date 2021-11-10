from loguru import logger
from sqlalchemy.orm import Session

from inventory.models import AccountsModel, ItemsModel
from inventory.schemas import Account, BaseAccount, Task, TaskBase


# def add_task(db: Session, task: Task):
#     db.query(models.UserModel).filter(models.UserModel.id == user_id).first()

# def fetch_account_by_public_id(db: Session, public_id: str):
#     return AccountsModel.


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


def add_task(db: Session, task: TaskBase):
    logger.info(f"Add task: {task}")
    task = ItemsModel(
        account_id=task.account_id,
        title=task.title,
        description=task.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"task was added")

    return task


def get_tasks(db: Session):
    return db.query(ItemsModel).all()
