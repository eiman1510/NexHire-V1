from pydantic import BaseModel, EmailStr
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    username: str
    fullname: str
    hash_pass: str
    date_joined: datetime
    role: str


class HR(User):
    company_name: str | None = None


class Candidate(User):
    resume_url: str
    resume_key: str
    skills: list[str] = []
    experience: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class userSignup(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str
