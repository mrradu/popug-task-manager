from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from frontoffice.db import get_storage
from frontoffice.exeption import RequiresLoginException
from frontoffice.models import AccountsModel

SECRET_KEY = "e261e056dcffb0f89c4882636a7ff1873ebde65920e620f46e1d224fe0b88648"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
Типа библиотека для работы с JWT токенами.
"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    public_id: Optional[str] = None


def get_request_token(request: Request):
    authorization: str = request.cookies.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        return None
    return token


def get_current_user(
    token: str = Depends(get_request_token),
    storage=Depends(get_storage),
):
    if not token:
        return None

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        public_id: str = payload.get("public_id")

        if public_id is None:
            raise credentials_exception

    except JWTError:
        return None
        # raise credentials_exception

    token_data = TokenData(public_id=public_id)
    user = storage.user.get_user(public_id=token_data.public_id)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
    request: Request,
    current_user: AccountsModel = Depends(get_current_user),
):
    if not current_user and request.url.path == "/sign_in":
        return None

    if not current_user or not current_user.is_active:
        raise RequiresLoginException()
    return current_user
