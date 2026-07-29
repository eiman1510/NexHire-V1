from fastapi import APIRouter

from features.login import router as login_router
from features.admin.admin_handler import router as admin_router

app = APIRouter()

app.include_router(login_router)
app.include_router(admin_router)

