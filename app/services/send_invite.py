from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import json

from core.config import SCOPES, GOOGLE_CALENDER_TOKEN


# Get credentials from the JSON stored in the environment variable
def get_credentials():
    token_info = json.loads(GOOGLE_CALENDER_TOKEN)

    credentials = Credentials.from_authorized_user_info(
        token_info,
        SCOPES,
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    return credentials


# Set up the calendar invite logic here
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
        "start": {
            "dateTime": start_datetime,
            "timeZone": "Asia/Karachi",
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "Asia/Karachi",
        },
        "attendees": [{"email": candidate_email}],
    }

    return (
        service.events()
        .insert(
            calendarId="primary",
            body=event,
            sendUpdates="all",
        )
        .execute()
    )