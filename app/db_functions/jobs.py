"""
Job Database Functions Module

This module handles all database operations related to job postings.
It provides functions to create, retrieve, update, delete, and search for job postings
in the NexHire recruitment system.
"""

from bson import ObjectId
from core.database import jobs_collection  # MongoDB collection for storing job postings


def create_job(job_data: dict):
    """
    Create a new job posting in the database.
    
    Args:
        job_data (dict): Dictionary containing job details such as:
            - title: Job title/position name
            - description: Full job description
            - requirements: Skills and qualifications required
            - location: Job location
            - salary_range: Expected salary range
            - posted_by: HR user ID who created the job
            - posted_date: Timestamp of when job was posted
            - is_active: Whether the job is currently active
    
    Returns:
        InsertOneResult: MongoDB insert result with inserted_id
    """
    return jobs_collection.insert_one(job_data)


def find_job_by_field(field: str, value):
    """
    Find a job by any specific field.
    
    Generic search function to find a job by any field (e.g., title, location, posted_by).
    
    Args:
        field (str): Field name to search by (e.g., 'title', 'posted_by')
        value: Value to match for the field
    
    Returns:
        dict or None: First job document matching the criteria, None if not found
    """
    return jobs_collection.find_one({field: value})


def get_job_by_id(job_id: str):
    """
    Retrieve a specific job posting by its ID.
    
    Args:
        job_id (str): ID of the job (ObjectId)
    
    Returns:
        dict or None: Job document if found, None otherwise
    """
    return jobs_collection.find_one({"_id": ObjectId(job_id)})


def update_job_by_id(job_id: str, update_data: dict):
    """
    Update job posting details.
    
    Args:
        job_id (str): ID of the job (ObjectId)
        update_data (dict): Dictionary containing fields to update (e.g., {'title': 'New Title'})
    
    Returns:
        UpdateResult: MongoDB update result with modified_count
    """
    return jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})


def delete_job_by_id(job_id: str):
    """
    Delete a job posting from the database.
    
    Args:
        job_id (str): ID of the job (ObjectId)
    
    Returns:
        DeleteResult: MongoDB delete result with deleted_count
    """
    return jobs_collection.delete_one({"_id": ObjectId(job_id)})


def find_jobs_by_query(query: dict):
    """
    Find all jobs matching a query.
    
    Supports complex queries for filtering jobs by multiple criteria.
    Example: {'location': 'New York', 'is_active': True}
    
    Args:
        query (dict): MongoDB query dictionary with filters
    
    Returns:
        list: List of job documents matching the query
    """
    return list(jobs_collection.find(query))


def get_all_jobs():
    """
    Retrieve all job postings from the database.
    
    Returns:
        list: List of all job documents in the collection
    """
    return list(jobs_collection.find())
