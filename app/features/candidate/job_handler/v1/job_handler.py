from db_functions.jobs import find_jobs_by_query, get_all_jobs
from utils.response import api_response
from utils.serialization import serialize_mongo_documents
from logging_config import logger


# BOTH CAN CALL THIS API
# returns all jobs created
def get_job_details_helper():
    try:
        logger.info("Fetching all jobs")

        jobs = get_all_jobs()
        jobs = serialize_mongo_documents(jobs)

        logger.info(f"Successfully fetched {len(jobs)} jobs")

        return api_response(
            status_code=200,
            data=jobs,
            message="Job fetched successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception("Error while fetching all jobs")

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
            f"Fetching filtered jobs | "
            f"min_salary={min_sal}, "
            f"experience={experience}, "
            f"job_type={job_type}"
        )

        query = {}

        if min_sal is not None:
            query["pay"] = {"$gte": min_sal}

        if experience is not None:
            query["required_experience"] = {"$lte": experience}

        if job_type is not None:
            query["job_type"] = job_type

        jobs = find_jobs_by_query(query)
        jobs = serialize_mongo_documents(jobs)

        logger.info(f"Successfully fetched {len(jobs)} jobs matching filters")

        return api_response(
            status_code=200,
            data=jobs,
            message="Data Fetched Successfully",
            api_source="job handler in hr",
            error_code=0,
        )

    except Exception:
        logger.exception("Error while fetching filtered jobs")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="job handler in hr",
            error_code=1,
        )
