from fastapi import APIRouter

from inventory.api import account, items

api_router = APIRouter()
api_router.include_router(account.router, prefix="/account")
api_router.include_router(items.router, prefix="/items")
