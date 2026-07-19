from models.job import Job
from db_functions.user import find_user, find_email_in_admin
from db_functions.jobs import (
    insert_job,
    find_in_job,
    update_job_id,
    delete_job_id,
    get_all_jobs,
    get_jobs_by_query,
)
from datetime import datetime, timezone
from utils.response import api_response
from bson import ObjectId

# Hr Route
"""
This routes checks is user is an hr
if yes then allows the user to enter job detail and create a new job
"""


def add_job_v1(jobDate: Job, user):
    print(type(user))
    print(user)
    current_user = user["id"]

    existing_user = find_user("_id", ObjectId(current_user))
    admin_approved = find_email_in_admin(existing_user["email"])

    if not admin_approved:
        return api_response(
            status_code=403,
            data=None,
            message="User cannot create job",
            api_source="job handler in hr",
            error_code=1,
        )

    newJob = Job(
        title=jobDate.title,
        description=jobDate.description,
        last_date_to_apply=jobDate.last_date_to_apply,
        skills_required=jobDate.skills_required,
        required_experience=jobDate.required_experience,
        job_type=jobDate.job_type,
        created_at=datetime.now(timezone.utc),
        created_by=str(current_user),
        status="Open",
        pay=jobDate.pay,
    )

    insert_job(newJob)

    return api_response(
        status_code=200,
        data=newJob,
        message="Job created Successfully",
        api_source="job handler in hr",
        error_code=0,
    )


# ---------------------------------------------------------------------------------------
# HR ROUTE
"""
check if the current user is the creator of a job
only creator can edit/update his job
"""


def update_job_v1(
    job_id: str,
    status: str | None = None,
    last_date_to_apply: datetime | None = None,
    user=None,
):

    curr_job = find_in_job("_id", ObjectId(job_id))

    if not curr_job:
        return api_response(
            status_code=404,
            data=None,
            message="Job not found",
            api_source="job handler in hr",
            error_code=1,
        )

    if curr_job["created_by"] != user["id"]:
        return api_response(
            status_code=403,
            data=None,
            message="User cannot edit job",
            api_source="job handler in hr",
            error_code=1,
        )

    update_data = {}

    if status is not None:
        update_data["status"] = status

    if last_date_to_apply is not None:
        update_data["last_date_to_apply"] = last_date_to_apply

    if not update_data:
        return api_response(
            status_code=400,
            data=None,
            message="No fields provided to update",
            api_source="job handler in hr",
            error_code=1,
        )

    update_job_id(job_id, update_data)
    return api_response(
        status_code=200,
        data=update_data,
        message="Job Updated",
        api_source="job handler in hr",
        error_code=0,
    )


# -------------------------------------------------------------------
# HR ROUTE
"""
check if the current user is the creator of a job
only creator can delete his job
"""


def delete_job_v1(jobId: str, user):

    curr_job = find_in_job("_id", ObjectId(jobId))

    if not curr_job:
        return api_response(
            status_code=404,
            data=None,
            message="Job not found",
            api_source="job handler in hr",
            error_code=1,
        )

    if curr_job["created_by"] != user["id"]:
        return api_response(
            status_code=403,
            data=None,
            message="Only job creator can delete job",
            api_source="job handler in hr",
            error_code=1,
        )

    delete_job_id(jobId)

    return api_response(
        status_code=200,
        data=jobId,
        message="Job Deleted",
        api_source="job handler in hr",
        error_code=0,
    )


# ---------------------------------------------------------------------
# BOTH CAN CALL THIS API
# returns alls jobs created
def get_job_details_v1():
    jobs = get_all_jobs()
    return api_response(
        status_code=200,
        data=jobs,
        message="Job fetched successfully",
        api_source="job handler in hr",
        error_code=0,
    )


# -------------------------------------------------------------
# get a specific job by id
"""
no use case for now,will complete it if needed
"""

# def get_job_v1(jobId: str):

#     curr_job = find_in_job("_id",ObjectId(jobId))

#     if not curr_job:
#         return api_response(status_code=400,data=None,message="No fields provided to update",api_source="job handler in hr",error_code=1)

#     curr_job["_id"] = str(curr_job["_id"])

#     return api_response("/routes/job_handler/get_job",curr_job,"Job fetched successfully")
# --------------------------------------------------------------

# for getting jobs based on some specific filter


def get_filtered_jobs_v1(
    min_sal: int | None = None,
    experience: int | None = None,
    job_type: str | None = None,
):
    query = {}

    if min_sal is not None:
        query["pay"] = {"$gte": min_sal}

    if experience is not None:
        query["required_experience"] = {"$lte": experience}

    if job_type is not None:
        query["job_type"] = job_type

    jobs = get_jobs_by_query(query)

    return api_response(
        status_code=200,
        data=jobs,
        message="Data Fetched Successfully",
        api_source="job handler in hr",
        error_code=0,
    )


# ---------------------------------------------------------
# HR
# return all jobs created by an hr


def get_all_created_job_v1(user):
    print(user)
    query = {"created_by": user["id"]}

    jobs = get_jobs_by_query(query)

    return api_response(
        status_code=200,
        data=jobs,
        message="Jobs by hr fetched",
        api_source="job handler in hr",
        error_code=0,
    )
