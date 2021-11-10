from fastapi import APIRouter

from auth.api import user, auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(user.router, prefix="/user")
