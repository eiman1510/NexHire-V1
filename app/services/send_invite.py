# from google.oauth2.credentials import Credentials
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build

# import json

# from core.config import SCOPES, GOOGLE_CALENDER_TOKEN


# # Get credentials from the JSON stored in the environment variable
# def get_credentials():
#     token_info = json.loads(GOOGLE_CALENDER_TOKEN)

#     credentials = Credentials.from_authorized_user_info(
#         token_info,
#         SCOPES,
#     )

#     if credentials.expired and credentials.refresh_token:
#         credentials.refresh(Request())

#     return credentials


# # Set up the calendar invite logic here
# def create_calendar_event(
#     candidate_email: str,
#     title: str,
#     description: str,
#     start_datetime: str,
#     end_datetime: str,
# ):

#     service = build("calendar", "v3", credentials=get_credentials())

#     event = {
#         "summary": title,
#         "description": description,
#         "start": {
#             "dateTime": start_datetime,
#             "timeZone": "Asia/Karachi",
#         },
#         "end": {
#             "dateTime": end_datetime,
#             "timeZone": "Asia/Karachi",
#         },
#         "attendees": [{"email": candidate_email}],
#     }

#     return (
#         service.events()
#         .insert(
#             calendarId="primary",
#             body=event,
#             sendUpdates="all",
#         )
#         .execute()
#     )

import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from core.config import SCOPES, GOOGLE_CALENDER_TOKEN
from logging_config import logger


# Get credentials from the JSON stored in the environment variable
def get_credentials():
    try:
        logger.info("Loading Google Calendar credentials from environment")

        token_info = json.loads(GOOGLE_CALENDER_TOKEN)

        logger.info("Successfully parsed Google Calendar token")

        credentials = Credentials.from_authorized_user_info(
            token_info,
            SCOPES,
        )

        logger.info("Google credentials object created")

        if credentials.expired:
            logger.info("Google credentials have expired")

        if credentials.expired and credentials.refresh_token:
            logger.info("Refreshing Google access token")
            credentials.refresh(Request())
            logger.info("Google access token refreshed successfully")

        logger.info("Returning Google credentials")
        return credentials

    except Exception as e:
        logger.exception(f"Failed to create Google credentials: {e}")
        raise


# Set up the calendar invite logic here
def create_calendar_event(
    candidate_email: str,
    title: str,
    description: str,
    start_datetime: str,
    end_datetime: str,
):
    try:
        logger.info("Building Google Calendar service")

        service = build("calendar", "v3", credentials=get_credentials())

        logger.info("Google Calendar service built successfully")

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

        logger.info(
            f"Creating calendar event for {candidate_email} "
            f"from {start_datetime} to {end_datetime}"
        )

        response = (
            service.events()
            .insert(
                calendarId="primary",
                body=event,
                sendUpdates="all",
            )
            .execute()
        )

        logger.info(
            f"Calendar event created successfully. Event ID: {response.get('id')}"
        )

        return response

    except Exception as e:
        logger.exception(f"Failed to create calendar event: {e}")
        raise