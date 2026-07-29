"""
Allowed HR Database Functions Module

This module handles all database operations related to HR user authorization and management.
It is used in the admin dashboard to manage which users are authenticated as HR personnel
and track their registration status in the NexHire recruitment system.
"""

from core.database import allowed_hr_collection  # MongoDB collection for storing approved HR users


def create_admin(email):
    """
    Create a new HR authorization entry for an employee.
    
    This function is called by an admin to authorize a user to act as an HR personnel.
    The HR user will need to complete their registration before they can access HR features.
    
    Args:
        email (str): Email address of the employee being authorized as HR
    
    Returns:
        InsertOneResult: MongoDB insert result with inserted_id
    
    Side Effects:
        - Creates an entry in allowed_hr_collection
        - Sets 'registered' flag to False initially (user must complete registration)
    """
    return allowed_hr_collection.insert_one({
        "email": email,
        "registered": False
    })


def delete_admin(email):
    """
    Remove HR authorization from an employee.
    
    This function revokes HR privileges from a user. Called by admin to deactivate
    an HR account or remove an HR user from the system.
    
    Args:
        email (str): Email address of the HR user to remove authorization from
    
    Returns:
        DeleteResult: MongoDB delete result with deleted_count
    
    Side Effects:
        - Removes the entry from allowed_hr_collection
        - User will no longer have access to HR features
    """
    return allowed_hr_collection.delete_one({
        "email": email
    })


def get_admins():
    """
    Retrieve all authorized HR users (both registered and unregistered).
    
    This function returns all HR accounts that have been approved by the admin,
    regardless of their registration status. Used in the admin dashboard to display
    the complete list of HR users.
    
    Returns:
        list: List of all HR authorization documents containing:
            - email: HR user's email address
            - registered: Boolean indicating if they completed registration
            - Other metadata if available
    """
    admins = list(allowed_hr_collection.find())
    return admins


def get_registered():
    """
    Retrieve all registered and active HR users.
    
    Returns only HR users who have completed their registration and activated their accounts.
    These are the active HR personnel who can access the platform.
    
    Returns:
        list: List of registered HR documents with:
            - email: HR user's email address
            - registered: True (filtered to only include registered users)
            - Other metadata if available
    """
    registered = list(allowed_hr_collection.find({"registered": True}))
    return registered
