from inventory.service.tasks import TasksDB
from inventory.service.user import UserDB


class Storage:
    def __init__(self, db):
        self.user = UserDB(db=db)
        self.tasks = TasksDB(db=db)
