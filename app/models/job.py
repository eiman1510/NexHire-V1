from pydantic import BaseModel
from datetime import datetime


class Job(BaseModel):
    title: str
    description: str
    last_date_to_apply: datetime
    skills_required: list
    required_experience: int
    minimum_education: str
    threshold: float
    job_type: str
    created_at: datetime
    created_by: str
    status: str
    pay: int


class JobApply(BaseModel):
    candidate_id: str
    job_id: str
    parsed_resume: dict
    status: str
    is_active: bool = True
    applied_at: datetime
