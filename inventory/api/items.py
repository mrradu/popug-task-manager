from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from starlette.requests import Request

from inventory import service
from inventory.db import get_db, get_storage
from inventory.popug_jwt import get_current_active_user
from inventory.schemas import Task, TaskBase
from inventory.service import Storage

router = APIRouter()


@router.post("/add", response_model=Task)
def add_task(
    task: TaskBase,
    storage: Storage = Depends(get_storage),
):
    """Создание таска."""
    logger.info(router)
    task = storage.tasks.add_task(task=task)
    return task


@router.post("/get", response_model=List[Task])
def get_tasks(
    request: Request,
    storage: Storage = Depends(get_storage),
    # db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """Получение списка тасок."""
    # user = storage.user.get_user(public_id=current_user.public_id)
    tasks = storage.tasks.get_tasks(user=current_user)
    print(tasks)
    return tasks
