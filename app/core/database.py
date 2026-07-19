from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client["nexhire"]
users_collection = db["users"]
admin_collection = db["allowed_hr"]
jobs = db["jobs"]
jobs_applied_collection = db["jobs_applied"]
