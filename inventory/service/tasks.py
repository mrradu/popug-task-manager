from loguru import logger

from inventory.enums import UserRole
from inventory import models
from inventory.schemas import Account, Task, TaskBase
from inventory.service.base import BaseDB


class TasksDB(BaseDB):
    """Интерфейс для работы с хранилищем тасков."""

    def add_task(self, task: TaskBase):
        logger.info(f"Add task: {task}")
        task = models.ItemsModel(
            title=task.title,
            description=task.description,
        )
        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)
        logger.info(f"task {task.title} was added")

        return task

    def get_tasks(self, user: Account):
        query = self._db.query(models.ItemsModel)
        if user.role in [UserRole.ADMIN, UserRole.MANAGER]:
            query = query.filter(models.ItemsModel.account_id == user.id)

        return [Task.from_orm(task) for task in query.all()]
