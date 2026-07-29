import socket
import smtplib
from email.mime.text import MIMEText

from core.config import EMAIL_USER, EMAIL_PASSWORD
from logging_config import logger


def send_email(to_email, subject, body):
    logger.info("Inside email 1")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = to_email

    logger.info("Inside email 2")
    logger.info(f"EMAIL_USER: {EMAIL_USER}")

    # Test network connectivity
    try:
        logger.info("Testing connection to smtp.gmail.com:587")
        socket.create_connection(("smtp.gmail.com", 587), timeout=10)
        logger.info("SMTP socket connection successful")
    except Exception as e:
        logger.exception(f"SMTP socket connection failed: {e}")
        raise

    try:
        logger.info("Opening SMTP connection")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            logger.info("SMTP connection established")

            logger.info("Starting TLS")
            server.starttls()

            logger.info("Logging into Gmail")
            server.login(EMAIL_USER, EMAIL_PASSWORD)

            logger.info("Sending email")
            server.send_message(msg)

            logger.info("Email sent successfully")

    except Exception as e:
        logger.exception(f"Failed to send email: {e}")
        raise