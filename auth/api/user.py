from http.client import HTTPException
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import controller, schemas
from auth.db import get_db
from auth.events.business.user import send_update_user_role_event
from auth.events.cud.user import send_create_user_event, send_update_user_event

router = APIRouter()


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = controller.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = controller.create_user(db=db, user=user)

    send_create_user_event(user)

    return user


@router.post("/update")
def update_user(user_fields: schemas.UserUpdateFields, db: Session = Depends(get_db)):
    user = controller.update_user(db, user_fields=user_fields)

    send_update_user_event(user)

    if user_fields.role:
        send_update_user_role_event(user)

    return "ok"


@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # current_user: UserModel = Depends(get_current_active_user),
):
    users = controller.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
