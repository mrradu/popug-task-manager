from fastapi import APIRouter

from frontoffice.api import accounting, items

api_router = APIRouter()
api_router.include_router(accounting.router)
api_router.include_router(items.router)
