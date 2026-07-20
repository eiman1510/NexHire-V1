from fastapi import APIRouter

from features.login import router as login_router

app = APIRouter()

app.include_router(login_router)
