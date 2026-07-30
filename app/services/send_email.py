# import socket
# import smtplib
# from email.mime.text import MIMEText

# from core.config import EMAIL_USER, EMAIL_PASSWORD
# from logging_config import logger


# def send_email(to_email, subject, body):
#     logger.info("Inside email 1")

#     msg = MIMEText(body)
#     msg["Subject"] = subject
#     msg["From"] = EMAIL_USER
#     msg["To"] = to_email

#     logger.info("Inside email 2")
#     logger.info(f"EMAIL_USER: {EMAIL_USER}")

#     # Test network connectivity
#     try:
#         logger.info("Testing connection to smtp.gmail.com:587")
#         socket.create_connection(("smtp.gmail.com", 587), timeout=100)
#         logger.info("SMTP socket connection successful")
#     except Exception as e:
#         logger.exception(f"SMTP socket connection failed: {e}")
#         raise

#     try:
#         logger.info("Opening SMTP connection")
#         with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
#             logger.info("SMTP connection established")

#             logger.info("Starting TLS")
#             server.starttls()

#             logger.info("Logging into Gmail")
#             server.login(EMAIL_USER, EMAIL_PASSWORD)

#             logger.info("Sending email")
#             server.send_message(msg)

#             logger.info("Email sent successfully")

#     except Exception as e:
#         logger.exception(f"Failed to send email: {e}")
#         raise

# import resend

# from core.config import RESEND_API_KEY,EMAIL_USER

# resend.api_key = RESEND_API_KEY

# def send_email(to_email, subject, body):
#     resend.Emails.send(
#         {
#             "from": "onboarding@resend.dev",
#             "to": EMAIL_USER,
#             "subject": subject,
#             "text": body,
#         }
#     )

import base64
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from core.config import SCOPES, GOOGLE_CALENDER_TOKEN
from logging_config import logger


def get_credentials():
    try:
        logger.info("Loading Google credentials from environment")

        token_info = json.loads(GOOGLE_CALENDER_TOKEN)

        credentials = Credentials.from_authorized_user_info(
            token_info,
            SCOPES,
        )

        if credentials.expired and credentials.refresh_token:
            logger.info("Refreshing Google access token")
            credentials.refresh(Request())

        return credentials

    except Exception as e:
        logger.exception(f"Failed to create Google credentials: {e}")
        raise


def send_email(
    recipient_email: str,
    subject: str,
    html_body: str,
):
    try:
        logger.info("Building Gmail service")

        service = build(
            "gmail",
            "v1",
            credentials=get_credentials(),
        )

        logger.info("Gmail service built successfully")

        message = MIMEMultipart("alternative")

        # "me" tells Gmail to use the authenticated account
        message["To"] = recipient_email
        message["Subject"] = subject

        message.attach(MIMEText(html_body, "html"))

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        logger.info(f"Sending email to {recipient_email}")

        response = (
            service.users()
            .messages()
            .send(
                userId="me",
                body={
                    "raw": raw_message,
                },
            )
            .execute()
        )

        logger.info(
            f"Email sent successfully. Message ID: {response['id']}"
        )

        return response

    except Exception as e:
        logger.exception(f"Failed to send email: {e}")
        raise