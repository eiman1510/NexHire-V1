import os
import boto3

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
REGION = os.getenv("AWS_REGION")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

SERVICE_ACCOUNT_FILE = BASE_DIR / "google_calendar_secret.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

MONGO_URL = os.getenv("MONGO_URL")

FEATURES = {
    "candidate:apply_job": "v1",
    "candidate:candidate_info": "v1",
    "candidate:job_handler": "v1",
    "candidate:signup": "v1",
    "hr:application_handler": "v1",
    "hr:job_handler": "v1",
    "hr:signup": "v1",
    "login": "v1",
    }

RESUME_API_KEY = os.getenv("RESUME_API_KEY")