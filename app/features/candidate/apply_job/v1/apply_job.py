from models.job import JobApply
from datetime import datetime, timezone
from db_functions.application import compare, insert_applied_job, fetch_my_jobs
from utils.response import api_response

# ---------------------------------------------------------
# CANDIDATE FUNCTION
"""
Checks whether a user has already applied for a job 
if not then apply for job else states already applied
"""


def job_apply_v1(job_id: str, user):

    candidate_id = user["id"]

    if not compare(job_id, candidate_id):
        return api_response(
            "apply_jobs/apply/{job_id}",
            None,
            "You have already applied for this job",
            409,
            1,
        )

    new_job = JobApply(
        candidate_id=candidate_id,
        job_id=job_id,
        status="Applied",
        applied_at=datetime.now(timezone.utc),
    )

    insert_applied_job(new_job)

    return api_response(
        status_code=200,
        data=new_job,
        message="Applied to job succesfully",
        api_source="candidate apply job",
    )


# ---------------------------------------------------------
# CANDIDATE FUNTION
"""
Return all job a specific user has applied for
"""


def get_applied_job_v1(user):
    result = fetch_my_jobs(user["id"])
    return api_response(
        status_code=200,
        data=result,
        message="Data Fetched Successfully",
        api_source="candidate get applied jobs",
    )
