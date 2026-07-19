from core.database import users_collection, admin_collection
from bson import ObjectId


def find_user(field, value):
    return users_collection.find_one({field: value})


# ---------------------------------------------------------------------------------------


def insert_in_user(new_user):
    return users_collection.insert_one(new_user.model_dump())


# ---------------------------------------------------------------------------------------


def find_email_in_admin(email):
    return admin_collection.find_one({"email": email})


# ---------------------------------------------------------------------------------------


def update_admin(email: str, update_data: dict):
    return admin_collection.update_one({"email": email}, {"$set": update_data})


# ---------------------------------------------------------------------------------------


def update_user(user_id, update_data:dict):
    return users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data}
    )

def get_profile_data(userid):
    candidate = users_collection.find_one(
            {"_id": ObjectId(userid)})

    if candidate:
        candidate["_id"] = str(candidate["_id"])
        candidate.pop("password", None)
    
    return candidate