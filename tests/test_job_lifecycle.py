import unittest
from unittest.mock import Mock, patch

from features.hr.job_handler.v1.job_handler import (
    activate_job_helper,
    delete_job_helper,
    update_job_helper,
)
from models.job import JobApply
from datetime import datetime, timedelta, timezone

JOB_ID = "507f1f77bcf86cd799439011"
HR_USER = {"id": "507f1f77bcf86cd799439012"}
JOB = {
    "_id": JOB_ID,
    "title": "Python Developer",
    "created_by": HR_USER["id"],
    "status": "Open",
    "last_date_to_apply": datetime.now(timezone.utc) + timedelta(days=7),
}


class JobLifecycleTests(unittest.TestCase):
    @patch("features.hr.job_handler.v1.job_handler.delete_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.job_inactive_email")
    @patch("features.hr.job_handler.v1.job_handler.get_user_profile_by_id")
    @patch("features.hr.job_handler.v1.job_handler.get_applications_by_job_id")
    @patch("features.hr.job_handler.v1.job_handler.set_job_applications_active")
    @patch("features.hr.job_handler.v1.job_handler.update_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.job_has_applications")
    @patch("features.hr.job_handler.v1.job_handler.find_job_by_field")
    def test_job_with_applications_is_closed_not_deleted(
        self,
        find_job,
        has_applications,
        update_job,
        set_active,
        get_applications,
        get_profile,
        send_inactive_email,
        delete_job,
    ):
        find_job.return_value = JOB
        has_applications.return_value = True
        set_active.return_value = Mock(modified_count=2)
        get_applications.return_value = [
            {"candidate_id": "candidate-1"},
            {"candidate_id": "candidate-2"},
        ]
        get_profile.side_effect = [
            {"fullname": "Candidate One", "email": "one@example.com"},
            {"fullname": "Candidate Two", "email": "two@example.com"},
        ]

        response = delete_job_helper(JOB_ID, HR_USER)

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["data"]["status"], "Closed")
        self.assertEqual(response["data"]["applications_deactivated"], 2)
        update_job.assert_called_once_with(JOB_ID, {"status": "Closed"})
        set_active.assert_called_once_with(JOB_ID, False)
        self.assertEqual(send_inactive_email.call_count, 2)
        delete_job.assert_not_called()

    @patch("features.hr.job_handler.v1.job_handler.delete_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.job_has_applications")
    @patch("features.hr.job_handler.v1.job_handler.find_job_by_field")
    def test_job_without_applications_is_deleted(
        self, find_job, has_applications, delete_job
    ):
        find_job.return_value = JOB
        has_applications.return_value = False
        delete_job.return_value = Mock()

        response = delete_job_helper(JOB_ID, HR_USER)

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["message"], "Job Deleted")
        delete_job.assert_called_once_with(JOB_ID)

    @patch("features.hr.job_handler.v1.job_handler.set_job_applications_active")
    @patch("features.hr.job_handler.v1.job_handler.update_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.find_job_by_field")
    def test_reopening_job_reactivates_applications(
        self, find_job, update_job, set_active
    ):
        find_job.return_value = {**JOB, "status": "Closed"}
        update_job.return_value = Mock()

        response = update_job_helper(JOB_ID, status="Open", user=HR_USER)

        self.assertEqual(response["status_code"], 200)
        set_active.assert_called_once_with(JOB_ID, True)

    @patch("features.hr.job_handler.v1.job_handler.set_job_applications_active")
    @patch("features.hr.job_handler.v1.job_handler.update_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.find_job_by_field")
    def test_activate_job_reopens_job_and_applications(
        self, find_job, update_job, set_active
    ):
        find_job.return_value = {**JOB, "status": "Closed"}
        set_active.return_value = Mock(modified_count=3)

        response = activate_job_helper(JOB_ID, HR_USER)

        self.assertEqual(response["status_code"], 200)
        self.assertEqual(response["data"]["status"], "Open")
        self.assertEqual(response["data"]["applications_activated"], 3)
        update_job.assert_called_once_with(JOB_ID, {"status": "Open"})
        set_active.assert_called_once_with(JOB_ID, True)

    @patch("features.hr.job_handler.v1.job_handler.set_job_applications_active")
    @patch("features.hr.job_handler.v1.job_handler.update_job_by_id")
    @patch("features.hr.job_handler.v1.job_handler.find_job_by_field")
    def test_activate_job_requires_future_deadline(
        self, find_job, update_job, set_active
    ):
        find_job.return_value = {
            **JOB,
            "status": "Closed",
            "last_date_to_apply": datetime.now(timezone.utc) - timedelta(days=1),
        }

        response = activate_job_helper(JOB_ID, HR_USER)

        self.assertEqual(response["status_code"], 400)
        update_job.assert_not_called()
        set_active.assert_not_called()

    def test_new_application_is_active_by_default(self):
        application = JobApply(
            candidate_id="candidate",
            job_id=JOB_ID,
            status="Applied",
            applied_at=datetime.now(timezone.utc),
        )

        self.assertTrue(application.is_active)


if __name__ == "__main__":
    unittest.main()
