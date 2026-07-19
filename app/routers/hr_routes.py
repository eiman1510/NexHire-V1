from fastapi import FastAPI

from features.hr.application_handler.route import router as application_handler_router
from features.hr.job_handler.route import router as job_handler_router
from features.hr.signup.route import router as hr_signup_router

app = FastAPI()

app.include_router(application_handler_router)
app.include_router(job_handler_router)
app.include_router(hr_signup_router)
