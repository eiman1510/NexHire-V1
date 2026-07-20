from fastapi import APIRouter

from features.hr.application_handler.route import router as application_handler_router
from app.features.hr.job_handler.route import router as job_handler_router
from features.hr.signup.route import router as hr_signup_router

app = APIRouter()

app.include_router(application_handler_router)
app.include_router(job_handler_router)
app.include_router(hr_signup_router)
