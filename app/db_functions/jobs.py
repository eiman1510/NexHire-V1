from bson import ObjectId

from core.database import jobs_collection


def create_job(job_data: dict):
    return jobs_collection.insert_one(job_data)


def find_job_by_field(field: str, value):
    return jobs_collection.find_one({field: value})


def get_job_by_id(job_id: str):
    return jobs_collection.find_one({"_id": ObjectId(job_id)})


def update_job_by_id(job_id: str, update_data: dict):
    return jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})


def delete_job_by_id(job_id: str):
    return jobs_collection.delete_one({"_id": ObjectId(job_id)})


def find_jobs_by_query(query: dict):
    return list(jobs_collection.find(query))


def get_all_jobs():
    return list(jobs_collection.find())
