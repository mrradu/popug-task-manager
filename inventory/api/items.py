from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inventory import controller
from inventory.db import get_db
from inventory.schemas import Task, TaskBase, Tasks

router = APIRouter()


@router.post("/add", response_model=Task)
def add_task(task: TaskBase, db: Session = Depends(get_db)):
    task = controller.add_task(db=db, task=task)
    return task


@router.post("/get", response_model=List[Task])
def get_tasks(db: Session = Depends(get_db)):
    tasks = controller.get_tasks(db=db)
    return tasks
