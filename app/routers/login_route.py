from fastapi import APIRouter

from features.login import router as login_router
# from features.test import router as test

app = APIRouter()

app.include_router(login_router)
# app.include_router(test)

