from pymongo import MongoClient
from .config import MONGO_URL

mongo_client = MongoClient(MONGO_URL)
database = mongo_client["nexhire"]

users_collection = database["users"]
allowed_hr_collection = database["allowed_hr"]
jobs_collection = database["jobs"]
job_applications_collection = database["jobs_applied"]
