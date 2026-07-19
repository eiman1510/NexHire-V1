from fastapi import APIRouter, Depends
from dependencies.get_user import get_current_user
from datetime import date, time
from .v1.application_handler import (
    schedule_interview_v1,
    reject_application_v1,
    send_hiring_email_v1,
    set_initial_meeting_v1,
    view_app_applications_v1
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
    user=Depends(get_current_user),
):
    return schedule_interview_v1(job_id, interview_date, interview_time, stat, user)


# ---------------------------------------------------------
# HR FUNCTION
"""
This rejects appliaction and send a rejection email
"""


@router.post("/reject_application")
def reject_application(job_id: str, user=Depends(get_current_user)):
    return reject_application_v1(job_id, user)


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
    user=Depends(get_current_user),
):
    return set_initial_meeting_v1(
        job_id, interview_link, interview_date, interview_time, user
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
    user=Depends(get_current_user),
):
    return send_hiring_email_v1(job_id, start, time, timings, working_days, pay, user)


@router.get("/application/{job_id}")
def view_app_application(job_id):
    return view_app_applications_v1(job_id)