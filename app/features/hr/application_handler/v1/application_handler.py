from datetime import date, time, datetime, timedelta
from bson import ObjectId

from db_functions.application import (
    add_interview_schedule_to_application,
    get_application_by_id,
    find_applications_by_job_id,
    update_application_status,
)
from db_functions.jobs import find_job_by_field
from db_functions.user import find_user_by_field, find_user_by_id
from utils.emails import (
    interview_email,
    rejection_email,
    online_assessment_email,
    hired_email,
)
from utils.response import api_response
from services.send_invite import create_calendar_event
from logging_config import logger
from utils.serialization import serialize_mongo_document


def get_application_email_context(application_id: str):
    application = get_application_by_id(application_id)
    if not application:
        return None

    candidate = find_user_by_field(
        "_id", ObjectId(application["candidate_id"])
    )
    job = find_job_by_field("_id", ObjectId(application["job_id"]))

    if not candidate or not job:
        return None

    return {
        "username": candidate["fullname"],
        "job_title": job["title"],
        "receiver_mail": candidate["email"],
        "job_id": application["job_id"],
    }

# ---------------------------------------------------------
# HR Helper function FUNCTION
"""
Change the current status of the application
not to be confused with the update function in job_handler as this one is different
this one first checks if user is job creator and then updates what state the
application is (applied, interview scheduled, interview done, rejected, hired)
"""


def update_job_status(job_id: str, stat: str, user_id):
    try:
        logger.info(
            f"Updating application status. Job ID: {job_id}, Status: {stat}, User ID: {user_id}"
        )

        application = get_application_by_id(job_id)
        job = None
        if application:
            job = find_job_by_field("_id", ObjectId(application["job_id"]))

        if not job or job["created_by"] != user_id:
            logger.warning(
                f"Unauthorized status update attempt. Job ID: {job_id}, User ID: {user_id}"
            )

            return api_response(
                status_code=401,
                data=None,
                message="User not permitted",
                api_source="application_handler",
                error_code=1,
            )

        update_application_status(job_id, stat)

        logger.info(f"Status updated successfully. Job ID: {job_id}, Status: {stat}")

        return True

    except Exception:
        logger.exception(f"Error updating status. Job ID: {job_id}, Status: {stat}")
        raise


# ---------------------------------------------------------
# HR FUNCTION
"""
This function schedules interviews and sends email to user about interview details
"""


def schedule_interview_helper(
    job_id: str,
    interview_date: date,
    interview_time: time,
    stat: str,
    user,
):
    try:
        logger.info(f"Interview scheduling initiated. Job ID: {job_id}")

        # --------------------------------------------------
        # Schedule Interview
        # --------------------------------------------------

        schedule_result = add_interview_schedule_to_application(
            job_id,
            str(interview_date),
            str(interview_time),
            stat,
        )

        if not schedule_result:
            logger.warning(
                f"Interview schedule could not be inserted. Job ID: {job_id}"
            )

            return api_response(
                status_code=400,
                data=None,
                message="Unable to schedule interview",
                api_source="application_handler",
                error_code=1,
            )

        logger.info(f"Interview schedule inserted successfully. Job ID: {job_id}")

        # --------------------------------------------------
        # Update Status
        # --------------------------------------------------

        status_result = update_job_status(
            job_id,
            "Interview Scheduled",
            user["id"],
        )

        if status_result is not True:
            logger.warning(f"Failed to update interview status. Job ID: {job_id}")

            return status_result

        # --------------------------------------------------
        # Get Candidate Data
        # --------------------------------------------------

        response = get_application_email_context(job_id)

        if not response:
            logger.warning(f"No candidate email data found. Job ID: {job_id}")

            return api_response(
                status_code=404,
                data=None,
                message="Candidate information not found",
                api_source="application_handler",
                error_code=1,
            )

        logger.info(f"Candidate email data retrieved. Job ID: {job_id}")

        # --------------------------------------------------
        # Send Email (Critical)
        # --------------------------------------------------

        try:
            interview_email(
                response["username"],
                response["receiver_mail"],
                response["job_title"],
                interview_date,
                interview_time,
            )

            logger.info(f"Interview email sent to {response['receiver_mail']}")

        except Exception:
            logger.exception(f"Failed to send interview email. Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Interview scheduled but email could not be sent",
                api_source="application_handler",
                error_code=1,
            )

        # --------------------------------------------------
        # Create Calendar Invite (Non-Critical)
        # --------------------------------------------------

        warnings = []

        try:
            start_dt = datetime.combine(
                interview_date,
                interview_time,
            )

            end_dt = start_dt + timedelta(hours=1)

            create_calendar_event(
                response["receiver_mail"],
                response["job_title"],
                "Onsite Interview",
                start_dt.isoformat(),
                end_dt.isoformat(),
            )

            logger.info(f"Calendar invite created for {response['receiver_mail']}")

        except Exception:
            logger.exception(f"Failed to create calendar invite. Job ID: {job_id}")

            warnings.append("Calendar invite could not be generated")

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        logger.info(f"Interview scheduled successfully. Job ID: {job_id}")

        return api_response(
            status_code=200,
            data={
                "candidate": response,
                "warnings": warnings,
            },
            message="Interview Scheduled Successfully",
            api_source="application_handler",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while scheduling interview. Job ID: {job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="application_handler",
            error_code=1,
        )


# ---------------------------------------------------------
# HR FUNCTION
"""
This rejects application and sends a rejection email
"""


def reject_application_helper(job_id: str, user):
    try:
        logger.info(f"Starting rejection process for Job ID: {job_id}")

        # --------------------------------------------------
        # Get Candidate Data
        # --------------------------------------------------

        response = get_application_email_context(job_id)

        if not response:
            logger.warning(f"No candidate data found for Job ID: {job_id}")

            return api_response(
                status_code=404,
                data=None,
                message="Candidate information not found",
                api_source="application_handler",
                error_code=1,
            )

        logger.info(f"Candidate data retrieved for Job ID: {job_id}")

        # --------------------------------------------------
        # Update Status (Critical)
        # --------------------------------------------------

        status_result = update_job_status(
            job_id,
            "Rejected",
            user["id"],
        )

        if status_result is not True:
            logger.warning(f"Failed to update rejection status. Job ID: {job_id}")

            return status_result

        logger.info(f"Application status updated to Rejected. Job ID: {job_id}")

        # --------------------------------------------------
        # Send Rejection Email
        # --------------------------------------------------

        try:
            rejection_email(
                response["username"],
                response["receiver_mail"],
                response["job_title"],
            )

            logger.info(
                f"Rejection email sent successfully to " f"{response['receiver_mail']}"
            )

        except Exception:
            logger.exception(f"Failed to send rejection email for Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Application rejected but email could not be sent",
                api_source="application_handler",
                error_code=1,
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        logger.info(f"Rejection process completed successfully. Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=response,
            message="Rejection mail sent",
            api_source="application_handler",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while rejecting application for Job ID: {job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="application_handler",
            error_code=1,
        )


# ---------------------------------------------------------
# HR FUNCTION
"""
This sets up the initial online test or online assessment
"""


def set_initial_meeting_helper(
    job_id: str,
    interview_link: str,
    interview_date: date,
    interview_time: time,
    user,
):
    try:
        logger.info(f"Starting initial assessment setup for Job ID: {job_id}")

        # --------------------------------------------------
        # Get Candidate Data
        # --------------------------------------------------

        if not interview_link or not interview_link.strip():
            logger.warning(f"Assessment link missing for Job ID: {job_id}")

            return api_response(
                status_code=400,
                data=None,
                message="Assessment link is required",
                api_source="application_handler",
                error_code=1,
            )

        response = get_application_email_context(job_id)

        if not response:
            logger.warning(f"No candidate data found for Job ID: {job_id}")

            return api_response(
                status_code=404,
                data=None,
                message="Candidate information not found",
                api_source="application_handler",
                error_code=1,
            )

        logger.info(f"Candidate data retrieved for Job ID: {job_id}")

        # --------------------------------------------------
        # Update Status
        # --------------------------------------------------

        status_result = update_job_status(
            job_id,
            "In Process",
            user["id"],
        )

        if status_result is not True:
            logger.warning(f"Failed to update application status. Job ID: {job_id}")

            return status_result

        logger.info(f"Application status updated to In Process. Job ID: {job_id}")

        # --------------------------------------------------
        # Send Assessment Email (Critical)
        # --------------------------------------------------

        try:
            online_assessment_email(
                response["username"],
                response["receiver_mail"],
                response["job_title"],
                interview_link,
                interview_date,
                interview_time,
            )

            logger.info(
                f"Assessment email sent successfully to " f"{response['receiver_mail']}"
            )

        except Exception:
            logger.exception(f"Failed to send assessment email for Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Assessment could not be sent",
                api_source="application_handler",
                error_code=1,
            )

        # --------------------------------------------------
        # Create Calendar Event (Non-Critical)
        # --------------------------------------------------

        try:
            start_dt = datetime.combine(
                interview_date,
                interview_time,
            )

            end_dt = start_dt + timedelta(hours=1)

            create_calendar_event(
                response["receiver_mail"],
                response["job_title"],
                "Initial Online Assessment",
                start_dt.isoformat(),
                end_dt.isoformat(),
            )

            logger.info(
                f"Assessment calendar event created for " f"{response['receiver_mail']}"
            )

        except Exception:
            logger.exception(
                f"Failed to create assessment calendar event for Job ID: {job_id}"
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        logger.info(f"Initial assessment scheduled successfully for Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=response,
            message="Initial assessment scheduled successfully",
            api_source="application_handler",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while scheduling assessment for Job ID: {job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="application_handler",
            error_code=1,
        )


# ---------------------------------------------------------
# HR FUNCTION
"""
Final hiring email
"""


def send_hiring_email_helper(
    job_id: str,
    start: date,
    time: time,
    timings: str,
    working_days: str,
    pay: int,
    user,
):
    try:
        logger.info(f"Starting hiring process for Job ID: {job_id}")

        # --------------------------------------------------
        # Validate Inputs
        # --------------------------------------------------

        if start < date.today():
            logger.warning(f"Invalid joining date for Job ID: {job_id}")

            return api_response(
                status_code=400,
                data=None,
                message="Joining date cannot be in the past",
                api_source="application_handler",
                error_code=1,
            )

        if pay <= 0:
            logger.warning(f"Invalid pay amount for Job ID: {job_id}")

            return api_response(
                status_code=400,
                data=None,
                message="Invalid pay amount",
                api_source="application_handler",
                error_code=1,
            )

        if not timings or not timings.strip():
            logger.warning(f"Missing timings for Job ID: {job_id}")

            return api_response(
                status_code=400,
                data=None,
                message="Timings are required",
                api_source="application_handler",
                error_code=1,
            )

        if not working_days or not working_days.strip():
            logger.warning(f"Missing working days for Job ID: {job_id}")

            return api_response(
                status_code=400,
                data=None,
                message="Working days are required",
                api_source="application_handler",
                error_code=1,
            )

        # --------------------------------------------------
        # Get Candidate Data
        # --------------------------------------------------

        response = get_application_email_context(job_id)

        if not response:
            logger.warning(f"No candidate data found for Job ID: {job_id}")

            return api_response(
                status_code=404,
                data=None,
                message="Candidate information not found",
                api_source="application_handler",
                error_code=1,
            )

        logger.info(f"Candidate data retrieved for Job ID: {job_id}")

        # --------------------------------------------------
        # Update Status
        # --------------------------------------------------

        status_result = update_job_status(
            job_id,
            "Hired",
            user["id"],
        )

        if status_result is not True:
            logger.warning(f"Failed to update status to Hired. Job ID: {job_id}")

            return status_result

        logger.info(f"Application status updated to Hired. Job ID: {job_id}")

        # --------------------------------------------------
        # Send Hiring Email (Critical)
        # --------------------------------------------------

        try:
            hired_email(
                response["username"],
                response["receiver_mail"],
                response["job_title"],
                start,
                timings,
                working_days,
                pay,
            )

            logger.info(
                f"Hiring email sent successfully to " f"{response['receiver_mail']}"
            )

        except Exception:
            logger.exception(f"Failed to send hiring email for Job ID: {job_id}")

            return api_response(
                status_code=500,
                data=None,
                message="Candidate marked as hired but email could not be sent",
                api_source="application_handler",
                error_code=1,
            )

        # --------------------------------------------------
        # Create Calendar Event (Non-Critical)
        # --------------------------------------------------

        try:
            start_dt = datetime.combine(start, time)
            end_dt = start_dt + timedelta(hours=1)

            create_calendar_event(
                response["receiver_mail"],
                response["job_title"],
                "Joining Date",
                start_dt.isoformat(),
                end_dt.isoformat(),
            )

            logger.info(
                f"Joining calendar event created for " f"{response['receiver_mail']}"
            )

        except Exception:
            logger.exception(
                f"Failed to create joining calendar event for Job ID: {job_id}"
            )

        # --------------------------------------------------
        # Success
        # --------------------------------------------------

        logger.info(f"Candidate hired successfully for Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=response,
            message="Candidate Hired",
            api_source="application_handler",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while hiring candidate for Job ID: {job_id}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="application_handler",
            error_code=1,
        )


# ---------------------------------------------------------
# HR FUNCTION
"""
View all applications for a job
"""


def view_app_applications_helper(job_id):
    try:
        logger.info(f"Fetching applications for Job ID: {job_id}")

        applications = find_applications_by_job_id(job_id)
        for application in applications:
            candidate = find_user_by_id(application["candidate_id"])
            application["candidate"] = serialize_mongo_document(
                candidate,
                excluded_fields={"hash_pass", "password"},
            )
            application["_id"] = str(application["_id"])

        logger.info(f"Retrieved {len(applications)} applications for Job ID: {job_id}")

        return api_response(
            status_code=200,
            data=applications,
            message="Application Retrieved successfully",
            api_source="hr application handler",
        )

    except Exception:
        logger.exception(f"Error retrieving applications for Job ID: {job_id}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="hr application handler",
            error_code=1,
        )
