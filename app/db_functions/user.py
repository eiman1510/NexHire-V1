"""
User Database Functions Module

This module handles all database operations related to users and HR personnel.
It provides functions to create, retrieve, and update user records and HR approvals
in the NexHire recruitment system.
"""

from bson import ObjectId
from core.database import allowed_hr_collection, users_collection  # MongoDB collections for users and approved HR


def find_user_by_field(field: str, value):
    """
    Find a user by any specific field.
    
    Generic search function to find a user by any field (e.g., email, username, role).
    
    Args:
        field (str): Field name to search by (e.g., 'email', 'username')
        value: Value to match for the field
    
    Returns:
        dict or None: User document if found, None otherwise
    """
    return users_collection.find_one({field: value})


def create_user(user_data: dict):
    """
    Create a new user in the database.
    
    Args:
        user_data (dict): Dictionary containing user details such as:
            - email: User's email address
            - password: Hashed password
            - name: Full name
            - role: User role ('candidate', 'hr', 'admin')
            - created_at: Timestamp of account creation
            - is_active: Whether the account is active
    
    Returns:
        InsertOneResult: MongoDB insert result with inserted_id
    """
    return users_collection.insert_one(user_data)


def find_allowed_hr_by_email(email: str):
    """
    Find an approved HR user by their email address.
    
    Checks the allowed_hr_collection to verify if an HR user is approved by admin.
    
    Args:
        email (str): Email address of the HR user
    
    Returns:
        dict or None: Approved HR document if found, None otherwise
    """
    return allowed_hr_collection.find_one({"email": email})


def update_allowed_hr_by_email(email: str, update_data: dict):
    """
    Update an approved HR user's information.
    
    Args:
        email (str): Email address of the HR user to update
        update_data (dict): Dictionary containing fields to update
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return allowed_hr_collection.update_one({"email": email}, {"$set": update_data})


def update_user_by_id(user_id: str, update_data: dict):
    """
    Update user information by their ID.
    
    Args:
        user_id (str): ID of the user (ObjectId)
        update_data (dict): Dictionary containing fields to update (e.g., {'profile': {...}})
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": update_data}
    )


def find_user_by_id(user_id: str):
    """
    Retrieve a specific user by their ID.
    
    Args:
        user_id (str): ID of the user (ObjectId)
    
    Returns:
        dict or None: User document if found, None otherwise
    """
    return users_collection.find_one({"_id": ObjectId(user_id)})
