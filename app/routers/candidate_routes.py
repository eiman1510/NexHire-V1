from fastapi import APIRouter

from features.candidate.apply_job.route import router as apply_job_router
from features.candidate.signup.route import router as candidate_signup_router
from features.candidate.candidate_info.route import router as candidate_info_router
from features.candidate.job_handler.route import router as job_handler_route

app = APIRouter()

app.include_router(apply_job_router)
app.include_router(candidate_signup_router)
app.include_router(candidate_info_router)
app.include_router(job_handler_route)
