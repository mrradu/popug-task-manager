from typing import List

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.orm import Session
from starlette.requests import Request

from inventory import service
from inventory.api.accounting import get_current_user
from inventory.db import get_db
from inventory.schemas import Task, TaskBase

router = APIRouter()


@router.post("/add", response_model=Task)
def add_task(task: TaskBase, db: Session = Depends(get_db)):
    """Создание таска."""
    logger.info(router)
    task = service.add_task(db=db, task=task)
    return task


@router.post("/get", response_model=List[Task])
def get_tasks(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Получение списка тасок."""
    user = service.get_user_with_public_id(public_id=current_user["public_id"], db=db)
    tasks = service.get_tasks(user=user, db=db)
    return tasks
