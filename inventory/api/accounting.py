from http import HTTPStatus

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from loguru import logger
from pydantic import BaseModel
from starlette import status
from starlette.responses import RedirectResponse

from inventory.auth import auth_gateway

router = APIRouter()

from starlette.requests import Request

class RequiresLoginException(Exception):
    pass


async def redirect() -> bool:
    raise RequiresLoginException


async def get_current_user(request: Request):
    try:
        user = auth_gateway.check_auth_user(request.cookies)
    except Exception:
        raise RequiresLoginException()
    return user.dict()
