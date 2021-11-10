from http import HTTPStatus

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from loguru import logger
from starlette import status
from starlette.responses import RedirectResponse

from frontoffice.exeption import RequiresLoginException
from frontoffice.gateway.auth import auth_gateway
from frontoffice.templates import templates

router = APIRouter()

from starlette.requests import Request


async def redirect() -> bool:
    raise RequiresLoginException


async def get_current_user(request: Request):
    try:
        user = auth_gateway.check_auth_user(request.cookies)
    except Exception:
        raise RequiresLoginException()
    print(user)
    return user.dict()


@router.get("/", response_class=HTMLResponse)
async def check(request: Request, current_user=Depends(get_current_user)):
    users = auth_gateway.get_users()
    return templates.TemplateResponse(
        "users.html",
        {
            "request": request,
            "users": users,
            "current_user": current_user,
        },
    )


@router.get("/sign_up", response_class=HTMLResponse)
def sign_up(request: Request):
    return templates.TemplateResponse("sign_up.html", {"request": request})


@router.post("/sign_up")
def sign_up_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    fullName: str = Form(...),
):
    auth_gateway.create_user(full_name=fullName, email=email, password=password)
    return RedirectResponse("/sign_in", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/sign_in", response_class=HTMLResponse)
def sign_up(request: Request):
    try:
        user = auth_gateway.check_auth_user(request.cookies)
        print(user)
        return RedirectResponse("/")
    except:
        return templates.TemplateResponse("sign_in.html", {"request": request})


@router.post("/sign_in", response_class=HTMLResponse)
def sign_up(
    request: Request,
    response: HTMLResponse,
    email: str = Form(...),
    password: str = Form(...),
):
    auth_response = auth_gateway.auth_user(email=email, password=password)

    if auth_response.status_code == HTTPStatus.UNAUTHORIZED:
        return templates.TemplateResponse(
            "sign_in.html",
            {"request": request, "error": True},
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    response = RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="Authorization", value=f"Bearer {auth_response.json()['access_token']}"
    )
    return response


@router.get("/{user_id}/edit", response_class=HTMLResponse)
def update_user(
    user_id: str,
    request: Request,
    current_user=Depends(get_current_user),
):
    return templates.TemplateResponse(
        "edit_user.html",
        {"request": request, "user_id": user_id, "current_user": current_user},
    )


@router.post("/{user_id}/edit", response_class=HTMLResponse)
def update_user(
    user_id: str,
    request: Request,
    current_user=Depends(get_current_user),
    role: str = Form(...),
    fullName: str = Form(...),
):

    auth_gateway.update_user(
        full_name=fullName,
        user_id=user_id,
        role=role,
    )
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
