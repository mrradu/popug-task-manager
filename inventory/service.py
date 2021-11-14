from loguru import logger
from sqlalchemy.orm import Session

from inventory.enums import UserRole
from inventory.models import AccountsModel, ItemsModel
from inventory.schemas import BaseAccount, Task, TaskBase


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
        is_active=True,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    logger.info(f"Account was added")

    return account


def add_task(db: Session, task: TaskBase):
    logger.info(f"Add task: {task}")
    task = ItemsModel(
        title=task.title,
        description=task.description,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info(f"task {task.title} was added")

    return task


def get_tasks(user: AccountsModel, db: Session):
    query = db.query(ItemsModel)
    if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        query = query.filter(ItemsModel.account_id == user.id)

    return [Task(task) for task in query.all()]


def get_user_with_public_id(public_id: int, db: Session) -> AccountsModel:
    """Получение данных пользователя по публичному идентификатору."""
    return db.query(AccountsModel).filter(AccountsModel.public_id == public_id).one()
