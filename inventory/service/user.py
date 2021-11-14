from loguru import logger

from inventory import models
from inventory.schemas import Account, AccountUpdateFields, BaseAccount
from inventory.service.base import BaseDB


class GetUserError(Exception):
    pass


class UserDB(BaseDB):
    """Интерфейс для работы с хранилищем юзеров."""

    def add_account(self, account: BaseAccount):
        """Добавление нового аккаунта в БД."""
        logger.info(f"Add account: {account}")
        account = models.AccountsModel(
            public_id=account.public_id,
            full_name=account.full_name,
            email=account.email,
            role=account.role,
        )
        self._db.add(account)
        self._db.commit()
        self._db.refresh(account)

        logger.info(f"Account was added")

        return account

    def get_user(self, public_id: str = None, id: int = None):
        """Получение юзера по email."""

        if public_id and id or not public_id and not id:

            raise GetUserError("One argument must be specified")
        user = self._db.query(models.AccountsModel)

        if public_id:
            user = user.filter(models.AccountsModel.public_id == public_id).first()

        if id:
            user = user.filter(models.AccountsModel.id == id).first()

        logger.info(f"USer: {user}")

        return Account.from_orm(user)

    def get_users(self):
        users = self._db.query(models.AccountsModel).all()
        return [Account.from_orm(user) for user in users]

    def update_user(self, user_fields: AccountUpdateFields):
        print(user_fields)
        print(user_fields.role)
        self._db.query(models.AccountsModel).filter(
            models.AccountsModel.public_id == user_fields.public_id
        ).update(user_fields.dict(exclude_none=True, exclude={"user_id"}))

        self._db.commit()

        return self.get_user(public_id=user_fields.public_id)
