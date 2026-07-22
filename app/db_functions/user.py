from bson import ObjectId

from core.database import allowed_hr_collection, users_collection


def find_user_by_field(field: str, value):
    return users_collection.find_one({field: value})


def create_user(user_data: dict):
    return users_collection.insert_one(user_data)


def find_allowed_hr_by_email(email: str):
    return allowed_hr_collection.find_one({"email": email})


def update_allowed_hr_by_email(email: str, update_data: dict):
    return allowed_hr_collection.update_one({"email": email}, {"$set": update_data})


def update_user_by_id(user_id: str, update_data: dict):
    return users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data}
    )


def find_user_by_id(user_id: str):
    return users_collection.find_one({"_id": ObjectId(user_id)})
