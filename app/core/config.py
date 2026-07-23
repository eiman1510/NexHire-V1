import os
import boto3

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


s3_client = boto3.client(
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

AFFINDA_API_KEY = os.getenv("AFFINDA_API_KEY")
AFFINDA_WORKSPACE_ID = os.getenv("AFFINDA_WORKSPACE_ID")
AFFINDA_RESUME_DOCUMENT_TYPE_ID = os.getenv(
    "AFFINDA_RESUME_DOCUMENT_TYPE_ID"
)
AFFINDA_JOB_DESCRIPTION_DOCUMENT_TYPE_ID = os.getenv(
    "AFFINDA_JOB_DESCRIPTION_DOCUMENT_TYPE_ID"
)
AFFINDA_BASE_URL = os.getenv("AFFINDA_BASE_URL") or "https://api.affinda.com/v3"
