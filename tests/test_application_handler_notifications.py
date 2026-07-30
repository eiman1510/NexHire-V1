import unittest
from datetime import date, time
from unittest.mock import patch

from features.hr.application_handler.v1.application_handler import schedule_interview_helper


class ApplicationHandlerNotificationTests(unittest.TestCase):
    @patch("features.hr.application_handler.v1.application_handler.create_calendar_event")
    @patch("features.hr.application_handler.v1.application_handler.interview_email")
    @patch("features.hr.application_handler.v1.application_handler.update_job_status")
    @patch("features.hr.application_handler.v1.application_handler.add_interview_schedule_to_application")
    @patch("features.hr.application_handler.v1.application_handler.get_application_email_context")
    def test_schedule_interview_fails_when_calendar_invite_cannot_be_sent(
        self,
        get_application_email_context,
        add_interview_schedule_to_application,
        update_job_status,
        interview_email,
        create_calendar_event,
    ):
        get_application_email_context.return_value = {
            "username": "Jane",
            "receiver_mail": "jane@example.com",
            "job_title": "Software Engineer",
            "job_id": "job-123",
        }
        add_interview_schedule_to_application.return_value = True
        update_job_status.return_value = True
        interview_email.return_value = None
        create_calendar_event.side_effect = Exception("calendar failure")

        result = schedule_interview_helper(
            job_id="job-123",
            interview_date=date(2026, 8, 1),
            interview_time=time(10, 0),
            stat="Interview Scheduled",
            user={"id": "hr-1"},
        )

        self.assertEqual(result["status_code"], 500)
        self.assertEqual(result["error_code"], 1)
        self.assertIn("calendar invite", result["message"].lower())


if __name__ == "__main__":
    unittest.main()
