from fastapi import FastAPI
from requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response

from frontoffice.api import api_router
from frontoffice.exeption import RequiresLoginException

app = FastAPI()

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return RedirectResponse("/sign_in")
