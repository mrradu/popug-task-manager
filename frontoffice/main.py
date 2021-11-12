from fastapi import FastAPI
from loguru import logger
from requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse, Response

from frontoffice import models
from frontoffice.api import api_router
from frontoffice.db import engine
from frontoffice.exeption import RequiresLoginException

models.Base.metadata.create_all(bind=engine)

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
    logger.info("Auth error. Redirect to sign_in page")
    return RedirectResponse("/sign_in")
