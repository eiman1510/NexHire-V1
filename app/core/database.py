from pymongo import MongoClient
from .config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["nexhire"]
users_collection = db["users"]
admin_collection = db["allowed_hr"]
jobs = db["jobs"]
jobs_applied_collection = db["jobs_applied"]
