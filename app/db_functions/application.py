"""
Application Database Functions Module

This module handles all database operations related to job applications.
It provides functions to create, retrieve, update, and manage candidate applications
to job postings in the NexHire recruitment system.
"""

from bson import ObjectId
from core.database import jobs_applied_collection  # MongoDB collection for storing job applications


def create_job_application(application_data: dict):
    """
    Create a new job application in the database.
    
    Args:
        application_data (dict): Dictionary containing application details such as:
            - job_id: ID of the job being applied for
            - candidate_id: ID of the candidate applying
            - applied_date: Timestamp of when application was submitted
            - status: Current status of the application (e.g., 'pending', 'reviewed')
    
    Returns:
        InsertOneResult: MongoDB insert result with inserted_id
    """
    return jobs_applied_collection.insert_one(application_data)


def find_application_by_job_and_candidate(job_id: str, candidate_id: str):
    """
    Find a specific application by job ID and candidate ID.
    
    Useful for checking if a candidate has already applied for a specific job.
    
    Args:
        job_id (str): ID of the job posting
        candidate_id (str): ID of the candidate
    
    Returns:
        dict or None: Application document if found, None otherwise
    """
    return jobs_applied_collection.find_one(
        {"job_id": job_id, "candidate_id": candidate_id}
    )


def count_job_applications(job_id: str):
    """
    Count the total number of applications for a specific job.
    
    Args:
        job_id (str): ID of the job posting
    
    Returns:
        int: Number of applications received for this job
    """
    return jobs_applied_collection.count_documents({"job_id": job_id})


def set_job_applications_active(job_id: str, is_active: bool):
    """
    Set the active status of all applications for a job.
    
    Used when a job posting is closed or reopened to update all related applications.
    
    Args:
        job_id (str): ID of the job posting
        is_active (bool): Whether applications should be active/visible
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return jobs_applied_collection.update_many(
        {"job_id": job_id},
        {"$set": {"is_active": is_active}},
    )


def find_applications_by_candidate_id(candidate_id: str):
    """
    Find all applications submitted by a specific candidate.
    
    Args:
        candidate_id (str): ID of the candidate
    
    Returns:
        list: List of application documents for this candidate
    """
    return list(
        jobs_applied_collection.find({"candidate_id": candidate_id})
    )


def update_application_status(application_id: str, status: str):
    """
    Update the status of an application.
    
    Common statuses: 'pending', 'reviewed', 'rejected', 'interview_scheduled', 'hired'
    
    Args:
        application_id (str): ID of the application (ObjectId)
        status (str): New status to set
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return jobs_applied_collection.update_one(
        {"_id": ObjectId(application_id)},
        {"$set": {"status": status}},
    )


def add_interview_schedule_to_application(
    application_id: str,
    interview_date,
    interview_time,
    interview_status: str,
):
    """
    Schedule an interview for an application and update its status.
    
    This function adds interview details to an application and marks its status as 'Interview Scheduled'.
    
    Args:
        application_id (str): ID of the application (ObjectId)
        interview_date: Date when the interview is scheduled
        interview_time: Time of the interview
        interview_status (str): Interview status (e.g., 'scheduled', 'completed', 'cancelled')
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return jobs_applied_collection.update_one(
        {"_id": ObjectId(application_id)},
        {
            "$set": {
                "status": "Interview Scheduled",
                "interview": {
                    "date": interview_date,
                    "time": interview_time,
                    "status": interview_status,
                },
            }
        },
    )


def get_application_by_id(application_id: str):
    """
    Retrieve a specific application by its ID.
    
    Args:
        application_id (str): ID of the application (ObjectId)
    
    Returns:
        dict or None: Application document if found, None otherwise
    """
    return jobs_applied_collection.find_one(
        {"_id": ObjectId(application_id)}
    )


def find_applications_by_job_id(job_id: str):
    """
    Find all applications for a specific job posting.
    
    Useful for HR users to view all candidates who applied for a job.
    
    Args:
        job_id (str): ID of the job posting
    
    Returns:
        list: List of all application documents for this job
    """
    return list(jobs_applied_collection.find({"job_id": job_id}))
