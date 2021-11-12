from fastapi import APIRouter

from inventory.api import items

api_router = APIRouter()
api_router.include_router(items.router, prefix="/items")
