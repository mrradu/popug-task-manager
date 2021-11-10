from fastapi import APIRouter, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse

from frontoffice.api.accounting import get_current_user
from frontoffice.gateway.items import item_gateway
from frontoffice.templates import templates

router = APIRouter()


@router.get("/items", response_class=HTMLResponse)
def get_items(request: Request, current_user=Depends(get_current_user)):
    tasks = item_gateway.get_tasks()
    return templates.TemplateResponse(
        "tasks.html", {"request": request, "tasks": tasks, "current_user": current_user}
    )
