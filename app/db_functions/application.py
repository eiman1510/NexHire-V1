from bson import ObjectId

from core.database import job_applications_collection


def create_job_application(application_data: dict):
    return job_applications_collection.insert_one(application_data)


def find_application_by_job_and_candidate(job_id: str, candidate_id: str):
    return job_applications_collection.find_one(
        {"job_id": job_id, "candidate_id": candidate_id}
    )


def count_job_applications(job_id: str):
    return job_applications_collection.count_documents({"job_id": job_id})


def set_job_applications_active(job_id: str, is_active: bool):
    return job_applications_collection.update_many(
        {"job_id": job_id},
        {"$set": {"is_active": is_active}},
    )


def find_applications_by_candidate_id(candidate_id: str):
    return list(
        job_applications_collection.find({"candidate_id": candidate_id})
    )


def update_application_status(application_id: str, status: str):
    return job_applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": status}},
    )


def add_interview_schedule_to_application(
    application_id: str,
    interview_date,
    interview_time,
    interview_status: str,
):
    return job_applications_collection.update_one(
        {"_id": ObjectId(application_id)},
        {
            "$set": {
                "status": "Interview Scheduled",
                "interview": {
                    "date": interview_date,
                    "time": interview_time,
                    "status": interview_status,
                },
            }
        },
    )


def get_application_by_id(application_id: str):
    return job_applications_collection.find_one(
        {"_id": ObjectId(application_id)}
    )


def find_applications_by_job_id(job_id: str):
    return list(job_applications_collection.find({"job_id": job_id}))
