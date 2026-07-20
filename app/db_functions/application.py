from core.database import jobs_applied_collection, jobs, users_collection
from bson import ObjectId
from models.job import JobApply
from .user import find_user
from .jobs import find_in_job


def insert_applied_job(job: JobApply):
    jobs_applied_collection.insert_one(job.model_dump())


# ---------------------------------------------------------


def compare(job_id: str, user_id: str):
    application = jobs_applied_collection.find_one(
        {"job_id": job_id, "candidate_id": user_id}
    )

    if application:
        return False

    return True


# ---------------------------------------------------------

def get_job_data(job_id):
    job = jobs.find_one({"_id": ObjectId(job_id)})

    if job:
        job["_id"] = str(job["_id"])
        return job
# ---------------------------------------------------------


def fetch_my_jobs(user_id: str):

    applications = list(jobs_applied_collection.find({"candidate_id": user_id}))

    for application in applications:
        application["_id"] = str(application["_id"])

    return applications


# ---------------------------------------------------------


def is_job_admin(application_id: str, user_id: str):

    application = jobs_applied_collection.find_one({"_id": ObjectId(application_id)})

    if application is None:
        return False

    job = jobs.find_one({"_id": ObjectId(application["job_id"]), "created_by": user_id})

    if job:
        return True
    return False


# ---------------------------------------------------------


def update_status(stat: str, job_id: str):
    result = jobs_applied_collection.update_one(
        {
            "_id": ObjectId(job_id),
        },
        {"$set": {"status": stat}},
    )
    return result


# ---------------------------------------------------------


def insert_interview_schedule(
    application_id: str, interview_date, interview_time, stat: str
):
    return jobs_applied_collection.update_one(
        {"_id": ObjectId(application_id)},
        {
            "$set": {
                "status": "Interview Scheduled",
                "interview": {
                    "date": str(interview_date),
                    "time": str(interview_time),
                    "status": stat,
                },
            }
        },
    )


# ---------------------------------------------------------


def get_email_data(application_id: str):
    application = jobs_applied_collection.find_one({"_id": ObjectId(application_id)})

    if not application:
        return None
    user = find_user("_id", ObjectId(application["candidate_id"]))
    job = find_in_job("_id", ObjectId(application["job_id"]))

    return {
        "username": user["fullname"],
        "job_title": job["title"],
        "receiver_mail": user["email"],
        "job_id": application["job_id"],
    }


# ---------------------------------------------------------


def get_my_applications(feild,job_id):
    applications = list(jobs_applied_collection.find({feild: job_id}))

    for application in applications:
        application["_id"] = str(application["_id"])

    return applications

# ---------------------------------------------------------


def fetch_candidate(candidate_id):
    candidate = users_collection.find_one(
            {"_id": ObjectId(candidate_id)}
        )

    if candidate:
        candidate["_id"] = str(candidate["_id"])
        candidate.pop("password", None)
    return candidate
