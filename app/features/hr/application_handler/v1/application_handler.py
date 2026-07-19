from datetime import date, time, datetime, timedelta
from db_functions.application import (
    is_job_admin,
    update_status,
    insert_interview_schedule,
    get_email_data,
    get_my_applications,
)
from utils.emails import (
    interview_email,
    rejection_email,
    online_assessment_email,
    hired_email,
)
from utils.response import api_response
from services.send_invite import create_calendar_event

# ---------------------------------------------------------
# HR Helper function FUNCTION
"""
Change the current status of the application
not to be confused with the update funtion in job_handler as this one is different 
this one 1st check is user is job creator and then update what state the application is (applied,interview scheduled,interview done,rejected,hired)
"""


def update_job_status(job_id: str, stat: str, user_id):
    if not is_job_admin(job_id, user_id):
        return api_response(status_code=401, data=None, message="User not permited")

    update_status(stat, job_id)


# ---------------------------------------------------------
# HR FUNCTION
"""
This function schedule interviews and send email to user about interview details
"""


def schedule_interview_v1(
    job_id: str,
    interview_date: date,
    interview_time: time,
    stat: str,
    user,
):
    insert_interview_schedule(job_id, interview_date, interview_time, stat)
    update_job_status(job_id, "Interview Scheduled", user["id"])
    responce = get_email_data(job_id)
    interview_email(
        responce["username"],
        responce["receiver_mail"],
        responce["job_title"],
        interview_date,
        interview_time,
    )
    start_dt = datetime.combine(interview_date, interview_time)
    end_dt = start_dt + timedelta(hours=1)
    create_calendar_event(
        responce["receiver_mail"],
        responce["job_title"],
        "Onsite Interview",
        start_dt.isoformat(),
        end_dt.isoformat(),
    )
    return api_response(
        status_code=200,
        data=responce,
        message="Interview Scheduled Successfully",
        api_source="application_handler",
    )


# ---------------------------------------------------------
# HR FUNCTION
"""
This rejects appliaction and send a rejection email
"""


def reject_application_v1(job_id: str, user):
    responce = get_email_data(job_id)
    update_job_status(job_id, "Rejected", user["id"])
    rejection_email(
        responce["username"], responce["receiver_mail"], responce["job_title"]
    )
    return api_response(
        status_code=200,
        data=responce,
        message="Rejection mail sent",
        api_source="application_handler",
    )


# ---------------------------------------------------------
# HR FUNCTION
"""
This sets up the initial online test or online application
"""


def set_initial_meeting_v1(
    job_id: str,
    interview_link: str,
    interview_date: date,
    interview_time: time,
    user,
):
    responce = get_email_data(job_id)
    update_job_status(job_id, "In Process", user["id"])
    online_assessment_email(
        responce["username"],
        responce["receiver_mail"],
        responce["job_title"],
        interview_link,
        interview_date,
        interview_time,
    )
    start_dt = datetime.combine(interview_date, interview_time)
    end_dt = start_dt + timedelta(hours=1)
    create_calendar_event(
        responce["receiver_mail"],
        responce["job_title"],
        "Initial Online Assesment",
        start_dt.isoformat(),
        end_dt.isoformat(),
    )
    return api_response(
        status_code=200,
        data=responce,
        message="initial test Scheduled Successfully",
        api_source="application_handler",
    )


# ---------------------------------------------------------
# HR FUNCTION
"""
final hiring email
"""


def send_hiring_email_v1(
    job_id: str,
    start: date,
    time: time,
    timings: str,
    working_days: str,
    pay: int,
    user,
):
    responce = get_email_data(job_id)
    update_job_status(job_id, "Hired", user["id"])
    hired_email(
        responce["username"],
        responce["receiver_mail"],
        responce["job_title"],
        start,
        timings,
        working_days,
        pay,
    )
    start_dt = datetime.combine(start, time)
    end_dt = start_dt + timedelta(hours=1)
    create_calendar_event(
        responce["receiver_mail"],
        responce["job_title"],
        "Joining Date",
        start_dt.isoformat(),
        end_dt.isoformat(),
    )
    return api_response(
        status_code=200,
        data=responce,
        message="Candidate Hired",
        api_source="application_handler",
    )


def view_app_applications_v1(job_id):
    result=get_my_applications(job_id)
    return api_response(status_code=200,data=result,message="Application Retrieved successfully",api_source="hr application handler")