from fastapi import APIRouter
from .v1.job_handler import get_job_details_helper, get_filtered_jobs_helper

router = APIRouter()


@router.get("/alljobs")
def get_job_details():
    return get_job_details_helper()


# -------------------------------------------------------------
# get a specific job by id
# @router.get("/getJob/{jobId}")
# def get_job(jobId: str):
#     pass
# --------------------------------------------------------------


# for getting jobs based on some specific filter
@router.get("/getFilteredJob")
def get_filtered_jobs(
    min_sal: int | None = None,
    experience: int | None = None,
    job_type: str | None = None,
):
    return get_filtered_jobs_helper(min_sal, experience, job_type)
