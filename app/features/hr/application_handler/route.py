from fastapi import APIRouter, Depends
from dependencies.get_api_content import get_request_context
from datetime import date, time
from .v1.application_handler import (
    reject_application_helper,
    schedule_interview_helper,
    send_hiring_email_helper,
    set_initial_meeting_helper,
    view_app_applications_helper,
)

router = APIRouter()


# ---------------------------------------------------------
# HR FUNCTION
"""
This function schedule interviews and send email to user about interview details
"""


@router.post("/schedule_interview")
def schedule_interview(
    job_id: str,
    interview_date: date,
    interview_time: time,
    stat: str,
    context=Depends(get_request_context()),
):
    print(context)
    return schedule_interview_helper(job_id, interview_date, interview_time, stat, context["user"])


# ---------------------------------------------------------
# HR FUNCTION
"""
This rejects appliaction and send a rejection email
"""


@router.post("/reject_application")
def reject_application(job_id: str, context=Depends(get_request_context())):
    print(context)
    return reject_application_helper(job_id, context["user"])


# ---------------------------------------------------------
# HR FUNCTION
"""
This sets up the initial online test or online application
"""


@router.post("/initial_meeting")
def set_initial_meeting(
    job_id: str,
    interview_link: str,
    interview_date: date,
    interview_time: time,
    context=Depends(get_request_context()),
):
    print(context)
    return set_initial_meeting_helper(
        job_id, interview_link, interview_date, interview_time, context["user"]
    )


# ---------------------------------------------------------
# HR FUNCTION
"""
final hiring email
"""


@router.post("/hiring_mail")
def send_hiring_email(
    job_id: str,
    start: date,
    time: time,
    timings: str,
    working_days: str,
    pay: int,
    context=Depends(get_request_context()),
):
    print(context)
    return send_hiring_email_helper(job_id, start, time, timings, working_days, pay, context["user"])


@router.get("/application/{job_id}")
def view_app_application(job_id):
    return view_app_applications_helper(job_id)
