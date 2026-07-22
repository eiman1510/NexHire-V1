from models.job import Job
from db_functions.user import find_allowed_hr_by_email, find_user_by_field
from db_functions.jobs import (
    create_job,
    delete_job_by_id,
    find_job_by_field,
    find_jobs_by_query,
    get_all_jobs,
    update_job_by_id,
)
from db_functions.application import (
    get_applications_by_job_id,
    job_has_applications,
    set_job_applications_active,
)
from db_functions.user import get_user_profile_by_id
from datetime import datetime, timezone
from utils.response import api_response
from bson import ObjectId
from logging_config import logger
from utils.emails import job_inactive_email

# Hr Route
"""
This routes checks is user is an hr
if yes then allows the user to enter job detail and create a new job
"""


def add_job_helper(job_data: Job, user):
    try:
        current_user = user["id"]

        logger.info(f"Job creation request received from user {current_user}")

        # --------------------------------------------------
        # Validate User
        # --------------------------------------------------

        existing_user = find_user_by_field(
            "_id",
            ObjectId(current_user),
        )

        if not existing_user:
            logger.warning(f"User not found. User ID: {current_user}")

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

        allowed_hr = find_allowed_hr_by_email(existing_user["email"])

        if not allowed_hr:
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

        if not job_data.title.strip():
            logger.warning(f"Empty job title provided by user {current_user}")

            return api_response(
                status_code=400,
                data=None,
                message="Job title is required",
                api_source="job handler in hr",
                error_code=1,
            )

        if job_data.pay <= 0:
            logger.warning(f"Invalid pay amount provided by user {current_user}")

            return api_response(
                status_code=400,
                data=None,
                message="Pay must be greater than zero",
                api_source="job handler in hr",
                error_code=1,
            )

        if job_data.last_date_to_apply <= datetime.now(timezone.utc):
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

        new_job = Job(
            title=job_data.title,
            description=job_data.description,
            last_date_to_apply=job_data.last_date_to_apply,
            skills_required=job_data.skills_required,
            required_experience=job_data.required_experience,
            job_type=job_data.job_type,
            created_at=datetime.now(timezone.utc),
            created_by=str(current_user),
            status="Open",
            pay=job_data.pay,
        )

        logger.info(f"Creating job '{job_data.title}' for user {current_user}")

        # --------------------------------------------------
        # Insert Job
        # --------------------------------------------------

        result = create_job(new_job)

        if result is None:
            logger.error(f"Job insertion failed for user {current_user}")

            return api_response(
                status_code=500,
                data=None,
                message="Unable to create job",
                api_source="job handler in hr",
                error_code=1,
            )

        logger.info(f"Job created successfully by user {current_user}")

        return api_response(
            status_code=200,
            data=new_job,
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


def update_job_helper(
    job_id: str,
    status: str | None = None,
    last_date_to_apply: datetime | None = None,
    user=None,
):
    try:
        logger.info(f"Job update requested. Job ID: {job_id}, User ID: {user['id']}")

        # --------------------------------------------------
        # Check Job Exists
        # --------------------------------------------------

        current_job = find_job_by_field(
            "_id",
            ObjectId(job_id),
        )

        if not current_job:
            logger.warning(f"Job not found. Job ID: {job_id}")

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

        if current_job["created_by"] != user["id"]:
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

        if status == "Open":
            return activate_job_helper(job_id, user, last_date_to_apply)

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
                logger.warning(f"Invalid status '{status}' for Job ID: {job_id}")

                return api_response(
                    status_code=400,
                    data=None,
                    message="Invalid job status",
                    api_source="job handler in hr",
                    error_code=1,
                )

            update_data["status"] = status

        if last_date_to_apply is not None:

            if last_date_to_apply <= datetime.now(timezone.utc):
                logger.warning(f"Invalid application deadline for Job ID: {job_id}")

                return api_response(
                    status_code=400,
                    data=None,
                    message="Last date to apply must be in the future",
                    api_source="job handler in hr",
                    error_code=1,
                )

            update_data["last_date_to_apply"] = last_date_to_apply

        if not update_data:
            logger.warning(f"No update fields provided. Job ID: {job_id}")

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

        result = update_job_by_id(
            job_id,
            update_data,
        )

        if not result:
            logger.error(f"Failed to update Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Failed to update job",
                api_source="job handler in hr",
                error_code=1,
            )

        if status in {"Closed", "Paused"}:
            set_job_applications_active(job_id, False)

        logger.info(f"Job updated successfully. Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=update_data,
            message="Job Updated",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(f"Unexpected error while updating Job ID: {job_id}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )


def activate_job_helper(
    job_id: str,
    user,
    last_date_to_apply: datetime | None = None,
):
    try:
        current_job = find_job_by_field("_id", ObjectId(job_id))

        if not current_job:
            return api_response(
                status_code=404,
                data=None,
                message="Job not found",
                api_source="job handler in hr",
                error_code=1,
            )

        if current_job["created_by"] != user["id"]:
            return api_response(
                status_code=403,
                data=None,
                message="Only the job creator can activate this job",
                api_source="job handler in hr",
                error_code=1,
            )

        if current_job.get("status") == "Open":
            return api_response(
                status_code=409,
                data=None,
                message="Job is already active",
                api_source="job handler in hr",
                error_code=1,
            )

        application_deadline = last_date_to_apply or current_job.get(
            "last_date_to_apply"
        )
        if application_deadline is None:
            return api_response(
                status_code=400,
                data=None,
                message="A future application deadline is required",
                api_source="job handler in hr",
                error_code=1,
            )

        if application_deadline.tzinfo is None:
            application_deadline = application_deadline.replace(tzinfo=timezone.utc)

        if application_deadline <= datetime.now(timezone.utc):
            return api_response(
                status_code=400,
                data=None,
                message="A new future application deadline is required",
                api_source="job handler in hr",
                error_code=1,
            )

        update_data = {"status": "Open"}
        if last_date_to_apply is not None:
            update_data["last_date_to_apply"] = last_date_to_apply

        update_job_by_id(job_id, update_data)
        application_update = set_job_applications_active(job_id, True)

        logger.info("Job %s and its applications were activated", job_id)

        return api_response(
            status_code=200,
            data={
                "job_id": job_id,
                "status": "Open",
                "applications_activated": application_update.modified_count,
                "last_date_to_apply": application_deadline,
            },
            message="Job activated successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception("Unexpected error while activating Job ID: %s", job_id)
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


def delete_job_helper(job_id: str, user):
    try:
        logger.info(f"Job deletion requested. Job ID: {job_id}, User ID: {user['id']}")

        # --------------------------------------------------
        # Check Job Exists
        # --------------------------------------------------

        current_job = find_job_by_field(
            "_id",
            ObjectId(job_id),
        )

        if not current_job:
            logger.warning(f"Job not found. Job ID: {job_id}")

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

        if current_job["created_by"] != user["id"]:
            logger.warning(
                f"Unauthorized delete attempt. Job ID: {job_id}, User ID: {user['id']}"
            )

            return api_response(
                status_code=403,
                data=None,
                message="Only job creator can delete job",
                api_source="job handler in hr",
                error_code=1,
            )

        if job_has_applications(job_id):
            update_job_by_id(job_id, {"status": "Closed"})
            application_update = set_job_applications_active(job_id, False)

            emails_sent = 0
            emails_failed = 0
            applications = get_applications_by_job_id(job_id)

            for application in applications:
                candidate = get_user_profile_by_id(application["candidate_id"])
                if not candidate or not candidate.get("email"):
                    emails_failed += 1
                    continue

                try:
                    job_inactive_email(
                        username=candidate["fullname"],
                        email=candidate["email"],
                        job_title=current_job["title"],
                    )
                    emails_sent += 1
                except Exception:
                    emails_failed += 1
                    logger.exception(
                        "Could not send inactive-job email to candidate %s",
                        application["candidate_id"],
                    )

            logger.info(
                "Job %s closed instead of deleted because it has applications",
                job_id,
            )

            return api_response(
                status_code=200,
                data={
                    "job_id": job_id,
                    "status": "Closed",
                    "applications_deactivated": application_update.modified_count,
                    "emails_sent": emails_sent,
                    "emails_failed": emails_failed,
                },
                message="Job has applications and was closed instead of deleted",
                api_source="job handler in hr",
                error_code=0,
            )

        # Jobs without applications can be permanently deleted.

        result = delete_job_by_id(job_id)

        if not result:
            logger.error(f"Failed to delete Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Failed to delete job",
                api_source="job handler in hr",
                error_code=1,
            )

        logger.info(f"Job deleted successfully. Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=job_id,
            message="Job Deleted",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception(f"Unexpected error while deleting Job ID: {job_id}")

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
def get_job_details_helper():
    try:
        logger.info("Fetching all available jobs")

        jobs = get_all_jobs()

        if not jobs:
            logger.info("No jobs found")

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(f"Retrieved {len(jobs)} jobs successfully")

        return api_response(
            status_code=200,
            data=jobs,
            message="Job fetched successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception("Unexpected error while fetching jobs")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )


# for getting jobs based on some specific filter


def get_filtered_jobs_helper(
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
                logger.warning(f"Invalid salary filter: {min_sal}")

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
                logger.warning(f"Invalid experience filter: {experience}")

                return api_response(
                    status_code=400,
                    data=None,
                    message="Experience cannot be negative",
                    api_source="job handler in hr",
                    error_code=1,
                )

            query["required_experience"] = {"$lte": experience}

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
                logger.warning(f"Invalid job type filter: {job_type}")

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

        jobs = find_jobs_by_query(query)

        if not jobs:
            logger.info("No jobs found matching filters")

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(f"Retrieved {len(jobs)} filtered jobs")

        return api_response(
            status_code=200,
            data=jobs,
            message="Data Fetched Successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception("Unexpected error while filtering jobs")

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


def get_all_created_job_helper(user):
    try:
        logger.info(f"Fetching jobs created by HR. User ID: {user['id']}")

        query = {"created_by": user["id"]}

        jobs = find_jobs_by_query(query)

        if not jobs:
            logger.info(f"No jobs found for HR User ID: {user['id']}")

            return api_response(
                status_code=200,
                data=[],
                message="No jobs found",
                api_source="job handler in hr",
                error_code=0,
            )

        logger.info(f"Retrieved {len(jobs)} jobs for HR User ID: {user['id']}")

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
