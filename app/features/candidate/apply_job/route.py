from fastapi import APIRouter, Depends
from dependencies.get_api_content import get_request_context
from .v1.apply_job import job_apply_v1, get_applied_job_v1

router = APIRouter()


@router.post("/apply/{job_id}")
def job_apply(
    job_id: str,
    context=Depends(get_request_context(job_apply_v1)),
    
):
    print(context)
    return job_apply_v1(job_id, context["user"])


@router.get("/my_jobs/{user_id}")
def get_applied_job(
    context=Depends(get_request_context(get_applied_job_v1)),
):
    print(context)
    return get_applied_job_v1(context["user"])
