from pydantic import BaseModel
from datetime import datetime


class Job(BaseModel):
    title: str
    description: str
    last_date_to_apply: datetime
    skills_required: list
    required_experience: int
    job_type: str
    created_at: datetime
    created_by: str
    status: str
    pay: int


class JobApply(BaseModel):
    candidate_id: str
    job_id: str
    # ats_percentage: float
    status: str
    applied_at: datetime
