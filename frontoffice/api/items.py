from fastapi import APIRouter, Depends, Form
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse

from frontoffice.api.accounting import get_current_user
from frontoffice.gateway.items import item_gateway
from frontoffice.popug_jwt import get_current_active_user
from frontoffice.templates import templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def get_items(request: Request, current_user=Depends(get_current_active_user)):
    tasks = item_gateway.get_tasks(cookies=request.cookies)
    return templates.TemplateResponse(
        "tasks.html", {"request": request, "tasks": tasks, "current_user": current_user}
    )


@router.post("/add", response_class=HTMLResponse)
def add_task(
    request: Request,
    task_title: str = Form(...),
    task_description: str = Form(...),
    current_user=Depends(get_current_active_user),
):
    item_gateway.add_tasks(task_title, task_description)

    return RedirectResponse("/items", status_code=status.HTTP_303_SEE_OTHER)
