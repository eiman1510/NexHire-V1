from core.database import jobs
from bson import ObjectId


def insert_job(jobDate):
    jobs.insert_one(jobDate.model_dump())


# ---------------------------------------------------------------------------------------


def find_in_job(field, value):
    return jobs.find_one({field: value})


# ---------------------------------------------------------------------------------------


def update_job_id(id, update_data):
    return jobs.update_one({"_id": ObjectId(id)}, {"$set": update_data})


# ---------------------------------------------------------------------------------------


def delete_job_id(jobid):
    jobs.delete_one({"_id": ObjectId(jobid)})


# ---------------------------------------------------------------------------------------


def get_jobs_by_query(query: dict):
    jobs_list = list(jobs.find(query))

    for job in jobs_list:
        job["_id"] = str(job["_id"])

    return jobs_list


# ---------------------------------------------------------------------------------------


def get_all_jobs():
    jobs_list = list(jobs.find())

    for job in jobs_list:
        job["_id"] = str(job["_id"])

    return jobs_list
