from loguru import logger
from sqlalchemy.orm import Session

from auth import models, schemas
from auth.schemas import UserUpdateFields
from auth.utils import get_password_hash


def get_user(db: Session, user_id: int) -> models.UserModel:
    """Получение юзера по идентификатору"""
    return db.query(models.UserModel).filter(models.UserModel.id == user_id).first()


def update_user(db: Session, user_fields: UserUpdateFields) -> models.UserModel:
    db.query(models.UserModel).filter(
        models.UserModel.public_id == user_fields.public_id
    ).update(user_fields.dict(exclude_none=True, exclude={"user_id"}))
    db.commit()

    return get_user_by_public_id(db=db, public_id=user_fields.public_id)


def get_user_by_email(db: Session, email: str):
    """Получение юзера по email."""
    logger.info(f"Email: {email}")
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


def get_user_by_public_id(db: Session, public_id: str):
    return (
        db.query(models.UserModel)
        .filter(models.UserModel.public_id == public_id)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Получение списка юзера."""
    logger.info(f"Get all users")
    return db.query(models.UserModel).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """Создание юзера."""
    db_user = models.UserModel(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
