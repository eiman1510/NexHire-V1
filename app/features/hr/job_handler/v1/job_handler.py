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
from logging_config import logger

# Hr Route
"""
This routes checks is user is an hr
if yes then allows the user to enter job detail and create a new job
"""

def add_job_v1(jobDate: Job, user):
    try:
        current_user = user["id"]

        logger.info(
            f"Job creation request received from user {current_user}"
        )

        # --------------------------------------------------
        # Validate User
        # --------------------------------------------------

        existing_user = find_user(
            "_id",
            ObjectId(current_user),
        )

        if not existing_user:
            logger.warning(
                f"User not found. User ID: {current_user}"
            )

            return api_response(
                status_code=404,
                data=None,
                message="User not found",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Validate HR Approval
        # --------------------------------------------------

        admin_approved = find_email_in_admin(
            existing_user["email"]
        )

        if not admin_approved:
            logger.warning(
                f"Unauthorized job creation attempt by {existing_user['email']}"
            )

            return api_response(
                status_code=403,
                data=None,
                message="User cannot create job",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Validate Job Data
        # --------------------------------------------------

        if not jobDate.title.strip():
            logger.warning(
                f"Empty job title provided by user {current_user}"
            )

            return api_response(
                status_code=400,
                data=None,
                message="Job title is required",
                api_source="job handler in hr",
                error_code=1,
            )

        if jobDate.pay <= 0:
            logger.warning(
                f"Invalid pay amount provided by user {current_user}"
            )

            return api_response(
                status_code=400,
                data=None,
                message="Pay must be greater than zero",
                api_source="job handler in hr",
                error_code=1,
            )

        if jobDate.last_date_to_apply <= datetime.now(
            timezone.utc
        ):
            logger.warning(
                f"Invalid application deadline provided by user {current_user}"
            )

            return api_response(
                status_code=400,
                data=None,
                message="Last date to apply must be in the future",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Create Job Object
        # --------------------------------------------------

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

        logger.info(
            f"Creating job '{jobDate.title}' for user {current_user}"
        )

        # --------------------------------------------------
        # Insert Job
        # --------------------------------------------------

        result = insert_job(newJob)

        if not result:
            logger.error(
                f"Job insertion failed for user {current_user}"
            )

            return api_response(
                status_code=500,
                data=None,
                message="Unable to create job",
                api_source="job handler in hr",
                error_code=1,
            )

        logger.info(
            f"Job created successfully by user {current_user}"
        )

        return api_response(
            status_code=200,
            data=newJob,
            message="Job created Successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            f"Unexpected error while creating job for user {user.get('id')}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
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
    try:
        logger.info(
            f"Job update requested. Job ID: {job_id}, User ID: {user['id']}"
        )

        # --------------------------------------------------
        # Check Job Exists
        # --------------------------------------------------

        curr_job = find_in_job(
            "_id",
            ObjectId(job_id),
        )

        if not curr_job:
            logger.warning(
                f"Job not found. Job ID: {job_id}"
            )

            return api_response(
                status_code=404,
                data=None,
                message="Job not found",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Verify Ownership
        # --------------------------------------------------

        if curr_job["created_by"] != user["id"]:
            logger.warning(
                f"Unauthorized job update attempt. Job ID: {job_id}, User ID: {user['id']}"
            )

            return api_response(
                status_code=403,
                data=None,
                message="User cannot edit job",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Build Update Data
        # --------------------------------------------------

        update_data = {}

        if status is not None:

            valid_status = [
                "Open",
                "Closed",
                "Paused",
            ]

            if status not in valid_status:
                logger.warning(
                    f"Invalid status '{status}' for Job ID: {job_id}"
                )

                return api_response(
                    status_code=400,
                    data=None,
                    message="Invalid job status",
                    api_source="job handler in hr",
                    error_code=1,
                )

            update_data["status"] = status

        if last_date_to_apply is not None:

            if last_date_to_apply <= datetime.now(
                timezone.utc
            ):
                logger.warning(
                    f"Invalid application deadline for Job ID: {job_id}"
                )

                return api_response(
                    status_code=400,
                    data=None,
                    message="Last date to apply must be in the future",
                    api_source="job handler in hr",
                    error_code=1,
                )

            update_data["last_date_to_apply"] = (
                last_date_to_apply
            )

        if not update_data:
            logger.warning(
                f"No update fields provided. Job ID: {job_id}"
            )

            return api_response(
                status_code=400,
                data=None,
                message="No fields provided to update",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Update Job
        # --------------------------------------------------

        result = update_job_id(
            job_id,
            update_data,
        )

        if not result:
            logger.error(
                f"Failed to update Job ID: {job_id}"
            )

            return api_response(
                status_code=500,
                data=None,
                message="Failed to update job",
                api_source="job handler in hr",
                error_code=1,
            )

        logger.info(
            f"Job updated successfully. Job ID: {job_id}"
        )

        return api_response(
            status_code=200,
            data=update_data,
            message="Job Updated",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            f"Unexpected error while updating Job ID: {job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )


# -------------------------------------------------------------------
# HR ROUTE
"""
check if the current user is the creator of a job
only creator can delete his job
"""


def delete_job_v1(jobId: str, user):
    try:
        logger.info(
            f"Job deletion requested. Job ID: {jobId}, User ID: {user['id']}"
        )

        # --------------------------------------------------
        # Check Job Exists
        # --------------------------------------------------

        curr_job = find_in_job(
            "_id",
            ObjectId(jobId),
        )

        if not curr_job:
            logger.warning(
                f"Job not found. Job ID: {jobId}"
            )

            return api_response(
                status_code=404,
                data=None,
                message="Job not found",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Verify Ownership
        # --------------------------------------------------

        if curr_job["created_by"] != user["id"]:
            logger.warning(
                f"Unauthorized delete attempt. Job ID: {jobId}, User ID: {user['id']}"
            )

            return api_response(
                status_code=403,
                data=None,
                message="Only job creator can delete job",
                api_source="job handler in hr",
                error_code=1,
            )

        # --------------------------------------------------
        # Delete Job
        # --------------------------------------------------

        result = delete_job_id(jobId)

        if not result:
            logger.error(
                f"Failed to delete Job ID: {jobId}"
            )

            return api_response(
                status_code=500,
                data=None,
                message="Failed to delete job",
                api_source="job handler in hr",
                error_code=1,
            )

        logger.info(
            f"Job deleted successfully. Job ID: {jobId}"
        )

        return api_response(
            status_code=200,
            data=jobId,
            message="Job Deleted",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            f"Unexpected error while deleting Job ID: {jobId}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )


# ---------------------------------------------------------------------
# BOTH CAN CALL THIS API
# returns alls jobs created
def get_job_details_v1():
    try:
        logger.info(
            "Fetching all available jobs"
        )

        jobs = get_all_jobs()

        if not jobs:
            logger.info(
                "No jobs found"
            )

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(
            f"Retrieved {len(jobs)} jobs successfully"
        )

        return api_response(
            status_code=200,
            data=jobs,
            message="Job fetched successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            "Unexpected error while fetching jobs"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
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
    try:
        logger.info(
            f"Filtering jobs. Salary={min_sal}, Experience={experience}, JobType={job_type}"
        )

        query = {}

        # --------------------------------------------------
        # Validate Salary
        # --------------------------------------------------

        if min_sal is not None:

            if min_sal < 0:
                logger.warning(
                    f"Invalid salary filter: {min_sal}"
                )

                return api_response(
                    status_code=400,
                    data=None,
                    message="Minimum salary cannot be negative",
                    api_source="job handler in hr",
                    error_code=1,
                )

            query["pay"] = {"$gte": min_sal}

        # --------------------------------------------------
        # Validate Experience
        # --------------------------------------------------

        if experience is not None:

            if experience < 0:
                logger.warning(
                    f"Invalid experience filter: {experience}"
                )

                return api_response(
                    status_code=400,
                    data=None,
                    message="Experience cannot be negative",
                    api_source="job handler in hr",
                    error_code=1,
                )

            query["required_experience"] = {
                "$lte": experience
            }

        # --------------------------------------------------
        # Validate Job Type
        # --------------------------------------------------

        if job_type is not None:

            valid_job_types = [
                "Full Time",
                "Part Time",
                "Internship",
                "Contract",
            ]

            if job_type not in valid_job_types:
                logger.warning(
                    f"Invalid job type filter: {job_type}"
                )

                return api_response(
                    status_code=400,
                    data=None,
                    message="Invalid job type",
                    api_source="job handler in hr",
                    error_code=1,
                )

            query["job_type"] = job_type

        # --------------------------------------------------
        # Fetch Jobs
        # --------------------------------------------------

        jobs = get_jobs_by_query(query)

        if not jobs:
            logger.info(
                "No jobs found matching filters"
            )

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(
            f"Retrieved {len(jobs)} filtered jobs"
        )

        return api_response(
            status_code=200,
            data=jobs,
            message="Data Fetched Successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            "Unexpected error while filtering jobs"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )


# ---------------------------------------------------------
# HR
# return all jobs created by an hr


def get_all_created_job_v1(user):
    try:
        logger.info(
            f"Fetching jobs created by HR. User ID: {user['id']}"
        )

        query = {
            "created_by": user["id"]
        }

        jobs = get_jobs_by_query(query)

        if not jobs:
            logger.info(
                f"No jobs found for HR User ID: {user['id']}"
            )

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(
            f"Retrieved {len(jobs)} jobs for HR User ID: {user['id']}"
        )

        return api_response(
            status_code=200,
            data=jobs,
            message="Jobs by hr fetched",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(
            f"Unexpected error while fetching jobs for HR User ID: {user['id']}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )
