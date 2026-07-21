from fastapi import APIRouter
from models.job import Job
from fastapi import Depends
from dependencies.get_api_content import get_request_context
from .v1.job_handler import (
    add_job_v1,
    update_job_v1,
    delete_job_v1,
    get_job_details_v1,
    get_all_created_job_v1,
    get_filtered_jobs_v1,
)
from datetime import datetime

router = APIRouter()


@router.post("/add_job")
def add_job(
    jobDate: Job,
    context=Depends(get_request_context(add_job_v1)),
):
    print(context)
    return add_job_v1(jobDate, context["user"])


# ---------------------------------------------------------------------------------------


@router.put("/update_job")
def update_job(
    job_id: str,
    status: str | None = None,
    last_date_to_apply: datetime | None = None,
    context=Depends(get_request_context(update_job_v1)),
):
    print(context)
    return update_job_v1(job_id, status, last_date_to_apply,context["user"])


# -------------------------------------------------------------------


@router.delete("/delete_job")
def delete_job(jobId: str, context=Depends(get_request_context(delete_job_v1))):
    print(context)
    return delete_job_v1(jobId, context["user"])


# ---------------------------------------------------------------------


@router.get("/alljobs")
def get_job_details():
    return get_job_details_v1()


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
    return get_filtered_jobs_v1(min_sal, experience, job_type)


# ---------------------------------------------------------
# HR
# return all jobs created by an hr
@router.get("/my_created_jobs")
def get_all_created_job(context=Depends(get_request_context(get_all_created_job_v1))):
    print(context)
    return get_all_created_job_v1(context["user"])
