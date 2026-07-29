"""
this is the job hanlder in candidate
candidate can view all jobs and even search job based on some filter
"""

from fastapi import APIRouter
from .v1.job_handler import get_filtered_jobs_helper, get_job_details_helper

router = APIRouter()


@router.get("/alljobs")
def get_candidate_jobs():
    return get_job_details_helper()


# for getting jobs based on some specific filter
@router.get("/get_filtered_job")
def get_filtered_candidate_jobs(
    min_sal: int | None = None,
    experience: int | None = None,
    job_type: str | None = None,
):
    return get_filtered_jobs_helper(min_sal, experience, job_type)
