from fastapi import APIRouter, Depends
from dependencies.get_user import get_current_user
from .v1.apply_job import job_apply_v1, get_applied_job_v1

router = APIRouter()


@router.post("/apply/{job_id}")
def job_apply(
    job_id: str,
    user=Depends(get_current_user),
):
    return job_apply_v1(job_id, user)


@router.get("/my_jobs/{user_id}")
def get_applied_job(
    user=Depends(get_current_user),
):
    return get_applied_job_v1(user)
