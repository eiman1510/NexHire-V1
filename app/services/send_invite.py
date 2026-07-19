from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from core.config import SCOPES

BASE_DIR = Path(__file__).resolve().parent.parent
TOKEN_FILE = BASE_DIR / "token.json"


def get_credentials():
    credentials = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

        with open(TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    return credentials


def create_calendar_event(
    candidate_email: str,
    title: str,
    description: str,
    start_datetime: str,
    end_datetime: str,
):

    service = build("calendar", "v3", credentials=get_credentials())

    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_datetime, "timeZone": "Asia/Karachi"},
        "end": {"dateTime": end_datetime, "timeZone": "Asia/Karachi"},
        "attendees": [{"email": candidate_email}],
    }

    return (
        service.events()
        .insert(calendarId="primary", body=event, sendUpdates="all")
        .execute()
    )
