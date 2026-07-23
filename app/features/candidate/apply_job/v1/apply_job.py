from models.job import JobApply
from datetime import datetime, timezone
from db_functions.application import (
    create_job_application,
    find_application_by_job_and_candidate,
    find_applications_by_candidate_id,
)
from db_functions.jobs import get_job_by_id
from db_functions.user import find_user_by_id
from services.generate_ats_json import (
    calculate_ats_score,
    format_resume_data,
    parse_resume_from_s3_url,
)
from services.storage import get_file_url
from utils.response import api_response
from utils.serialization import serialize_mongo_document
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

        candidate = find_user_by_id(candidate_id)
        resume_key = candidate.get("resume_key") if candidate else None

        if not resume_key:
            return api_response(
                status_code=201,
                message="Please upload your resume before applying",
                data=None,
                api_source="candidate apply job",
                error_code=1,
            )

        if find_application_by_job_and_candidate(job_id, candidate_id):
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

        resume_url = get_file_url(resume_key)
        parser_response = parse_resume_from_s3_url(resume_url)
        parsed_resume = format_resume_data(parser_response)
        ats_result = calculate_ats_score(
            parsed_resume,
            job_id,
        )

        if not ats_result["selected"]:
            return api_response(
                status_code=202,
                message="You are not eligible for this job",
                data=ats_result,
                api_source="candidate apply job",
                error_code=1,
            )

        new_job = JobApply(
            candidate_id=candidate_id,
            job_id=job_id,
            parsed_resume=parsed_resume,
            status="Applied",
            applied_at=datetime.now(timezone.utc),
        )

        create_job_application(new_job.model_dump())

        logger.info(
            f"Application submitted successfully. Candidate={candidate_id}, Job={job_id}"
        )

        return api_response(
            status_code=200,
            data={
                "application": new_job.model_dump(),
                "parsed_resume": parsed_resume,
            },
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

        applications = find_applications_by_candidate_id(candidate_id)
        for application in applications:
            job = get_job_by_id(application["job_id"])
            application["job"] = serialize_mongo_document(job)
            application["_id"] = str(application["_id"])

        logger.info(f"Applied jobs fetched successfully for candidate {candidate_id}")

        return api_response(
            status_code=200,
            data=applications,
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
