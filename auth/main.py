from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from auth import models
from auth.api import api_router
from auth.db import engine

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
