"""
The route page for candidate:apply job 
which handles the operations where candidate apply for job and see jobs he/she has applied
"""


from fastapi import APIRouter, Depends


from dependencies.get_api_content import get_request_context
from .v1.apply_job import job_apply_helper, get_applied_job_helper

router = APIRouter()

@router.post("/apply/{job_id}")
def job_apply(
    job_id: str,
    context=Depends(get_request_context()),
):
    return job_apply_helper(job_id, context["user"])


@router.get("/my_jobs/{user_id}")
def get_applied_jobs(context=Depends(get_request_context())):
    return get_applied_job_helper(context["user"])
