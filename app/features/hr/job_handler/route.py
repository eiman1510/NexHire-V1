from fastapi import APIRouter
from models.job import Job
from fastapi import Depends
from dependencies.get_api_content import get_request_context
from dependencies.get_version import load_function
from datetime import datetime

router = APIRouter()


@router.post("/add_job")
def add_job(
    jobDate: Job,
    context=Depends(get_request_context()),
):
    print(context)
    add_job_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="add_job_helper",
    )
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
    update_job_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="update_job_helper",
    )
    return update_job_helper(job_id, status, last_date_to_apply,context["user"])


# -------------------------------------------------------------------


@router.delete("/delete_job")
def delete_job(jobId: str, context=Depends(get_request_context())):
    print(context)
    delete_job_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="delete_job_helper",
    )
    return delete_job_helper(jobId, context["user"])


# ---------------------------------------------------------------------


@router.get("/alljobs")
def get_job_details():
    get_job_details_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="get_job_details_helper",
    )
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
    get_filtered_jobs_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="get_filtered_jobs_helper",
    )
    return get_filtered_jobs_helper(min_sal, experience, job_type)


# ---------------------------------------------------------
# HR
# return all jobs created by an hr
@router.get("/my_created_jobs")
def get_all_created_job(context=Depends(get_request_context())):
    print(context)
    get_all_created_job_helper = load_function(
        feature_key="hr:job_handler",
        module_name="job_handler",
        function_name="get_all_created_job_helper",
    )
    return get_all_created_job_helper(context["user"])
