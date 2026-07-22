from fastapi import APIRouter
from models.job import Job
from fastapi import Depends
from dependencies.get_api_content import get_request_context
from datetime import datetime
from .v1.job_handler import (
    add_job_helper,
    delete_job_helper,
    get_all_created_job_helper,
    get_filtered_jobs_helper,
    get_job_details_helper,
    update_job_helper,
)

router = APIRouter()


@router.post("/add_job")
def add_job(
    jobDate: Job,
    context=Depends(get_request_context()),
):
    print(context)
    return add_job_helper(jobDate, context["user"])


# ---------------------------------------------------------------------------------------


@router.put("/update_job")
def update_job(
    job_id: str,
    status: str | None = None,
    last_date_to_apply: datetime | None = None,
    context=Depends(get_request_context()),
):
    print(context)
    return update_job_helper(job_id, status, last_date_to_apply,context["user"])


# -------------------------------------------------------------------


@router.delete("/delete_job")
def delete_job(jobId: str, context=Depends(get_request_context())):
    print(context)
    return delete_job_helper(jobId, context["user"])


# ---------------------------------------------------------------------


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


# ---------------------------------------------------------
# HR
# return all jobs created by an hr
@router.get("/my_created_jobs")
def get_all_created_job(context=Depends(get_request_context())):
    print(context)
    return get_all_created_job_helper(context["user"])
