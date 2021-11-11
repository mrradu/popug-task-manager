from sqlalchemy.orm import Session

from frontoffice import models


def get_user(db: Session, public_id: str):
    """Получение юзера по email."""
    return (
        db.query(models.AccountsModel)
        .filter(models.AccountsModel.public_id == public_id)
        .first()
    )
