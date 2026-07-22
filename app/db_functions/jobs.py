from bson import ObjectId

from core.database import jobs_collection


def create_job(job):
    return jobs_collection.insert_one(job.model_dump())


def find_job_by_field(field: str, value):
    return jobs_collection.find_one({field: value})


def get_job_by_id(job_id: str):
    job = jobs_collection.find_one({"_id": ObjectId(job_id)})

    if job:
        job["_id"] = str(job["_id"])

    return job


def update_job_by_id(job_id: str, update_data: dict):
    return jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})


def delete_job_by_id(job_id: str):
    return jobs_collection.delete_one({"_id": ObjectId(job_id)})


def find_jobs_by_query(query: dict):
    jobs = list(jobs_collection.find(query))

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jobs


def get_all_jobs():
    jobs = list(jobs_collection.find())

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jobs
