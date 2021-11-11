from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from auth.controller import get_user_by_public_id
from auth.db import get_db
from auth.models import UserModel

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


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
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
        raise credentials_exception

    token_data = TokenData(public_id=public_id)
    user = get_user_by_public_id(db, public_id=token_data.public_id)

    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
