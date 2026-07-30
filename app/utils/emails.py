from services.send_email import send_email


# def interview_email(
#     username: str, email: str, job_title: str, interview_date: str, interview_time: str
# ):
#     subject = f"Interview Invitation - {job_title}"

#     body = f"""
# Dear {username},

# Congratulations! You have been shortlisted for the position of {job_title}.

# Your interview has been scheduled as follows:

# Date: {interview_date}
# Time: {interview_time}

# Please ensure that you are available at the scheduled time.

# If you have any questions or need to reschedule, please contact us.

# Best regards,
# HR Team
# """

#     send_email(recipient_email=email, subject=subject, html_body=body)

def interview_email(
    username: str,
    email: str,
    job_title: str,
    interview_date: str,
    interview_time: str,
):
    subject = f"Interview Invitation - {job_title}"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {username},</p>

            <p>
                Congratulations! You have been shortlisted for the position of
                <strong>{job_title}</strong>.
            </p>

            <p>
                We are pleased to invite you to an interview. Please find the
                details below:
            </p>

            <h3>Interview Details</h3>

            <ul>
                <li><strong>Position:</strong> {job_title}</li>
                <li><strong>Date:</strong> {interview_date}</li>
                <li><strong>Time:</strong> {interview_time}</li>
            </ul>

            <p>
                Please ensure that you are available at the scheduled time and
                join the interview a few minutes early.
            </p>

            <p>
                If you have any questions or need to reschedule, please feel
                free to contact us.
            </p>

            <p>
                We look forward to speaking with you and wish you the very best
                of luck.
            </p>

            <br>

            <p>
                Best Regards,<br>
                Recruitment Team
            </p>
        </body>
    </html>
    """

    send_email(
        recipient_email=email,
        subject=subject,
        html_body=body,
    )
# -------------------------------------------------------------------------


# def rejection_email(username: str, email: str, job_title: str):
#     subject = f"Application Update - {job_title}"

#     body = f"""
# Dear {username},

# Thank you for your interest in the {job_title} position and for taking the time to participate in our hiring process.

# After careful consideration, we have decided to move forward with other candidates whose qualifications more closely match our current requirements.

# We appreciate the effort you invested in your application and encourage you to apply for future opportunities that match your skills and experience.

# We wish you the very best in your job search and future endeavors.

# Kind regards,
# HR Team
# """

#     send_email(recipient_email=email, subject=subject, html_body=body)

def rejection_email(username: str, email: str, job_title: str):
    subject = f"Application Update - {job_title}"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {username},</p>

            <p>
                Thank you for your interest in the
                <strong>{job_title}</strong> position and for taking the time
                to participate in our hiring process.
            </p>

            <p>
                After careful consideration, we have decided to move forward
                with other candidates whose qualifications more closely match
                our current requirements.
            </p>

            <p>
                We sincerely appreciate the time, effort, and interest you
                invested in your application. We encourage you to apply for
                future opportunities that align with your skills and experience.
            </p>

            <p>
                We wish you every success in your job search and future
                professional endeavors.
            </p>

            <br>

            <p>
                Kind Regards,<br>
                Recruitment Team
            </p>
        </body>
    </html>
    """

    send_email(
        recipient_email=email,
        subject=subject,
        html_body=body,
    )

# def job_inactive_email(username: str, email: str, job_title: str):
#     subject = f"Job Status Update - {job_title}"

#     body = f"""
# Dear {username},

# The {job_title} position is currently inactive.

# Your application has not been deleted. It will become active again automatically if the position is reopened.

# Thank you for your patience and interest in this opportunity.

# Best regards,
# HR Team
# """

#     send_email(recipient_email=email, subject=subject, html_body=body)

def job_inactive_email(username: str, email: str, job_title: str):
    subject = f"Job Status Update - {job_title}"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {username},</p>

            <p>
                Thank you for your interest in the
                <strong>{job_title}</strong> position.
            </p>

            <p>
                We would like to inform you that this position is currently
                <strong>inactive</strong> and is not accepting applications at
                this time.
            </p>

            <p>
                Please be assured that your application has <strong>not</strong>
                been deleted. If the position is reopened in the future, your
                application will automatically become active again for
                consideration.
            </p>

            <p>
                We appreciate your patience and continued interest in joining
                our team.
            </p>

            <br>

            <p>
                Best Regards,<br>
                Recruitment Team
            </p>
        </body>
    </html>
    """

    send_email(
        recipient_email=email,
        subject=subject,
        html_body=body,
    )

# -------------------------------------------------------------------------


# def online_assessment_email(
#     username,
#     receiver_mail,
#     job_title,
#     assessment_link,
#     assessment_date,
#     assessment_time,
# ):

#     subject = f"Online Assessment - {job_title}"

#     body = f"""
# Dear {username},

# Thank you for your interest in the {job_title} position.

# As the next step in our hiring process, you have been invited to complete an online assessment / meeting.

# Details:
# Date: {assessment_date}
# Time: {assessment_time}
# Link: {assessment_link}

# Please ensure that you join on time and have a stable internet connection.

# We wish you the best of luck and look forward to your participation.

# Best Regards,
# Recruitment Team
# """

#     send_email(recipient_email=receiver_mail, subject=subject, html_body=body)

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
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {username},</p>

            <p>
                Thank you for your interest in the
                <strong>{job_title}</strong> position.
            </p>

            <p>
                As the next step in our hiring process, you have been invited
                to complete an online assessment/meeting.
            </p>

            <h3>Assessment Details</h3>

            <ul>
                <li><strong>Position:</strong> {job_title}</li>
                <li><strong>Date:</strong> {assessment_date}</li>
                <li><strong>Time:</strong> {assessment_time}</li>
                <li>
                    <strong>Assessment Link:</strong>
                    <a href="{assessment_link}">
                        Join Assessment
                    </a>
                </li>
            </ul>

            <p>
                Please ensure that you join on time and have a stable internet
                connection before the assessment begins.
            </p>

            <p>
                We wish you the very best of luck and look forward to your
                participation.
            </p>

            <br>

            <p>
                Best Regards,<br>
                Recruitment Team
            </p>
        </body>
    </html>
    """

    send_email(
        recipient_email=receiver_mail,
        subject=subject,
        html_body=body,
    )


# -------------------------------------------------------------------------


# def hired_email(
#     username, receiver_mail, job_title, start_date, timing, working_days, pay
# ):

#     subject = f"Congratulations! Offer for {job_title}"

#     body = f"""
# Dear {username},

# Congratulations!

# We are pleased to inform you that you have been selected for the position of {job_title}.

# Employment Details:

# Position: {job_title}
# Start Date: {start_date}
# Working Hours: {timing}
# Working Days: {working_days}
# Compensation: {pay}

# We are excited to welcome you to our team and look forward to working with you.

# If you have any questions regarding your onboarding process, please feel free to contact us.

# Congratulations once again, and welcome aboard!

# Best Regards,
# Recruitment Team
# """

#     send_email(recipient_email=receiver_mail, subject=subject, html_body=body)


def hired_email(
    username,
    receiver_mail,
    job_title,
    start_date,
    timing,
    working_days,
    pay,
):
    subject = f"Congratulations! Offer for {job_title}"

    body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear {username},</p>

            <p><strong>Congratulations!</strong></p>

            <p>
                We are pleased to inform you that you have been selected
                for the position of <strong>{job_title}</strong>.
            </p>

            <h3>Employment Details</h3>

            <ul>
                <li><strong>Position:</strong> {job_title}</li>
                <li><strong>Start Date:</strong> {start_date}</li>
                <li><strong>Working Hours:</strong> {timing}</li>
                <li><strong>Working Days:</strong> {working_days}</li>
                <li><strong>Compensation:</strong> {pay}</li>
            </ul>

            <p>
                We are excited to welcome you to our team and look forward
                to working with you.
            </p>

            <p>
                If you have any questions regarding your onboarding process,
                please feel free to contact us.
            </p>

            <p>
                Congratulations once again, and welcome aboard!
            </p>

            <br>

            <p>
                Best Regards,<br>
                Recruitment Team
            </p>
        </body>
    </html>
    """

    send_email(
        recipient_email=receiver_mail,
        subject=subject,
        html_body=body,
    )