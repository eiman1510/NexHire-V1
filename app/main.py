from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

# from routers.hr_routes import app as hr_app
# from routers.candidate_routes import app as candidate_app
# from routers.login_route import app as login_app

# app = FastAPI()

# app.mount("/hr", hr_app)
# app.mount("/candidate", candidate_app)
# app.mount("/common", login_app)

from features.candidate.apply_job.route import router as apply_job_router
from features.candidate.signup.route import router as candidate_signup_router
from features.candidate.candidate_info.route import router as candidate_info_router
from features.candidate.job_handler.route import router as job_handler_route
from features.hr.application_handler.route import router as application_handler_router
from features.hr.job_handler.route import router as job_handler_router
from features.hr.signup.route import router as hr_signup_router
from features.login import router as login_router

app = FastAPI()

app.include_router(login_router)
app.include_router(hr_signup_router)
app.include_router(candidate_signup_router)
app.include_router(apply_job_router)
app.include_router(candidate_info_router)
app.include_router(job_handler_route)
app.include_router(application_handler_router)
app.include_router(job_handler_router)
