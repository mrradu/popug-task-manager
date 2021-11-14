from sqlalchemy.orm import Session


class BaseDB:
    def __init__(self, db: Session):
        self._db = db
