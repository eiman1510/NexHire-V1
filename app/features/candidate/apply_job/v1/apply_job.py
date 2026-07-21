from models.job import JobApply
from datetime import datetime, timezone
from db_functions.application import (
    compare,
    insert_applied_job,
    fetch_my_jobs,
    get_job_data,
)
from utils.response import api_response
from logging_config import logger

# ---------------------------------------------------------
# CANDIDATE FUNCTION
"""
Checks whether a user has already applied for a job
if not then apply for job else states already applied
"""


def job_apply_helper(job_id: str, user):
    try:
        candidate_id = user["id"]

        logger.info(f"Candidate {candidate_id} attempting to apply for job {job_id}")

        if not compare(job_id, candidate_id):
            logger.warning(
                f"Duplicate application attempt. Candidate={candidate_id}, Job={job_id}"
            )

            return api_response(
                status_code=409,
                message="You have already applied for this job",
                data=None,
                api_source="apply_jobs/apply/{job_id}",
                error_code=1,
            )

        new_job = JobApply(
            candidate_id=candidate_id,
            job_id=job_id,
            status="Applied",
            applied_at=datetime.now(timezone.utc),
        )

        insert_applied_job(new_job)

        logger.info(
            f"Application submitted successfully. Candidate={candidate_id}, Job={job_id}"
        )

        return api_response(
            status_code=200,
            data=new_job,
            message="Applied to job successfully",
            api_source="candidate apply job",
        )

    except Exception:
        logger.exception(
            f"Error while applying for job. Candidate={user.get('id')}, Job={job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="candidate apply job",
            error_code=1,
        )


# ---------------------------------------------------------
# CANDIDATE FUNCTION
"""
Return all jobs a specific user has applied for
"""


def get_applied_job_helper(user):
    try:
        candidate_id = user["id"]

        logger.info(f"Fetching applied jobs for candidate {candidate_id}")

        result = fetch_my_jobs(candidate_id)
        for application in result:
            job = get_job_data(application["job_id"])
            application["job"] = job

        logger.info(f"Applied jobs fetched successfully for candidate {candidate_id}")

        return api_response(
            status_code=200,
            data=result,
            message="Data Fetched Successfully",
            api_source="candidate get applied jobs",
        )

    except Exception:
        logger.exception(f"Error fetching applied jobs for candidate {user.get('id')}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="candidate get applied jobs",
            error_code=1,
        )
