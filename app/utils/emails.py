from services.send_email import send_email


def interview_email(
    username: str, email: str, job_title: str, interview_date: str, interview_time: str
):
    subject = f"Interview Invitation - {job_title}"

    body = f"""
Dear {username},

Congratulations! You have been shortlisted for the position of {job_title}.

Your interview has been scheduled as follows:

Date: {interview_date}
Time: {interview_time}

Please ensure that you are available at the scheduled time.

If you have any questions or need to reschedule, please contact us.

Best regards,
HR Team
"""

    send_email(to_email=email, subject=subject, body=body)


# -------------------------------------------------------------------------


def rejection_email(username: str, email: str, job_title: str):
    subject = f"Application Update - {job_title}"

    body = f"""
Dear {username},

Thank you for your interest in the {job_title} position and for taking the time to participate in our hiring process.

After careful consideration, we have decided to move forward with other candidates whose qualifications more closely match our current requirements.

We appreciate the effort you invested in your application and encourage you to apply for future opportunities that match your skills and experience.

We wish you the very best in your job search and future endeavors.

Kind regards,
HR Team
"""

    send_email(to_email=email, subject=subject, body=body)


# -------------------------------------------------------------------------


def online_assessment_email(
    username,
    receiver_mail,
    job_title,
    assessment_link,
    assessment_date,
    assessment_time,
):

    subject = f"Online Assessment - {job_title}"

    body = f"""
Dear {username},

Thank you for your interest in the {job_title} position.

As the next step in our hiring process, you have been invited to complete an online assessment / meeting.

Details:
Date: {assessment_date}
Time: {assessment_time}
Link: {assessment_link}

Please ensure that you join on time and have a stable internet connection.

We wish you the best of luck and look forward to your participation.

Best Regards,
Recruitment Team
"""

    send_email(receiver_mail, subject, body)


# -------------------------------------------------------------------------


def hired_email(
    username, receiver_mail, job_title, start_date, timing, working_days, pay
):

    subject = f"Congratulations! Offer for {job_title}"

    body = f"""
Dear {username},

Congratulations!

We are pleased to inform you that you have been selected for the position of {job_title}.

Employment Details:

Position: {job_title}
Start Date: {start_date}
Working Hours: {timing}
Working Days: {working_days}
Compensation: {pay}

We are excited to welcome you to our team and look forward to working with you.

If you have any questions regarding your onboarding process, please feel free to contact us.

Congratulations once again, and welcome aboard!

Best Regards,
Recruitment Team
"""

    send_email(receiver_mail, subject, body)
