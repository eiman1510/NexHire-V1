from fastapi import APIRouter
from dependencies.get_version import load_function

router = APIRouter()


@router.get("/alljobs")
def get_job_details():
    get_job_details_helper = load_function(
        feature_key="candidate:job_handler",
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
        feature_key="candidate:job_handler",
        module_name="job_handler",
        function_name="get_filtered_jobs_helper",
    )
    return get_filtered_jobs_helper(min_sal, experience, job_type)
