"""Entry point of the application."""

import logging
import sys

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import route_auth, route_solver
from app.config import project_settings

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


app = FastAPI(docs_url="/api/docs", **project_settings)


@app.get("/")
async def root():
    """Basic root."""
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(route_auth.router)
app.include_router(route_solver.router)
