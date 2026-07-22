from bson import ObjectId

from core.database import job_applications_collection, jobs_collection
from models.job import JobApply
from .jobs import find_job_by_field
from .user import find_user_by_field


def create_job_application(application: JobApply):
    return job_applications_collection.insert_one(application.model_dump())


def candidate_has_applied(job_id: str, candidate_id: str) -> bool:
    application = job_applications_collection.find_one(
        {"job_id": job_id, "candidate_id": candidate_id}
    )
    return application is not None


def job_has_applications(job_id: str) -> bool:
    return job_applications_collection.count_documents({"job_id": job_id}, limit=1) > 0


def set_job_applications_active(job_id: str, is_active: bool):
    return job_applications_collection.update_many(
        {"job_id": job_id},
        {"$set": {"is_active": is_active}},
    )


def get_applications_by_candidate_id(candidate_id: str):
    applications = list(
        job_applications_collection.find({"candidate_id": candidate_id})
    )

    for application in applications:
        application["_id"] = str(application["_id"])

    return applications


def is_application_owned_by_hr(application_id: str, hr_user_id: str) -> bool:
    application = job_applications_collection.find_one(
        {"_id": ObjectId(application_id)}
    )
    if application is None:
        return False

    job = jobs_collection.find_one(
        {
            "_id": ObjectId(application["job_id"]),
            "created_by": hr_user_id,
        }
    )
    return job is not None


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
                    "date": str(interview_date),
                    "time": str(interview_time),
                    "status": interview_status,
                },
            }
        },
    )


def get_application_email_context(application_id: str):
    application = job_applications_collection.find_one(
        {"_id": ObjectId(application_id)}
    )
    if not application:
        return None

    candidate = find_user_by_field("_id", ObjectId(application["candidate_id"]))
    job = find_job_by_field("_id", ObjectId(application["job_id"]))

    return {
        "username": candidate["fullname"],
        "job_title": job["title"],
        "receiver_mail": candidate["email"],
        "job_id": application["job_id"],
    }


def get_applications_by_job_id(job_id: str):
    applications = list(job_applications_collection.find({"job_id": job_id}))

    for application in applications:
        application["_id"] = str(application["_id"])

    return applications
