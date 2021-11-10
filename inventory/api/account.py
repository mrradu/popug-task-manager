from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from inventory import controller
from inventory.db import get_db
from inventory.schemas import Account, BaseAccount

router = APIRouter()


@router.post("/create", response_model=Account)
def create_user(account: BaseAccount, db: Session = Depends(get_db)):
    account = controller.add_account(db=db, account=account)

    return account
