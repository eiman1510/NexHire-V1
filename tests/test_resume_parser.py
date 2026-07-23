import unittest
from unittest.mock import Mock, patch

from features.test import test_resume_parser
from services.generate_ats_json import (
    build_affinda_documents_url,
    format_affinda_resume,
    parse_resume_from_s3_url,
)


class ResumeParserTests(unittest.TestCase):
    def test_affinda_response_is_reduced_to_clean_values(self):
        response = {
            "data": {
                "candidateName": {"raw": "EIMAN ASIF"},
                "email": [{"parsed": "eimanasif15@gmail.com"}],
                "phoneNumber": [
                    {"parsed": {"formattedNumber": "+92 307 9438798"}}
                ],
                "location": {
                    "parsed": {
                        "formatted": "Lahore, Punjab, Pakistan",
                        "city": "Lahore",
                        "state": "Punjab",
                        "country": "Pakistan",
                        "countryCode": "PK",
                        "latitude": 31.5203696,
                        "longitude": 74.3587473,
                        "rawInput": "excluded field",
                    }
                },
                "education": [],
                "workExperience": [],
                "skill": [
                    {
                        "raw": "Python,",
                        "parsed": {
                            "name": "Python (Programming Language)",
                            "isSoftware": True,
                        },
                    }
                ],
                "hobby": [{"parsed": "Cloud,"}],
            }
        }

        result = format_affinda_resume(response)

        self.assertEqual(result["candidateName"], "EIMAN ASIF")
        self.assertEqual(result["email"], "eimanasif15@gmail.com")
        self.assertEqual(result["phoneNumber"], "+92 307 9438798")
        self.assertNotIn("rawInput", result["location"])
        self.assertEqual(result["skill"], ["Python", "Cloud Computing"])

    def test_affinda_documents_url_includes_api_version(self):
        self.assertEqual(
            build_affinda_documents_url("https://api.affinda.com"),
            "https://api.affinda.com/v3/documents",
        )
        self.assertEqual(
            build_affinda_documents_url("https://api.affinda.com/v3"),
            "https://api.affinda.com/v3/documents",
        )
        self.assertEqual(
            build_affinda_documents_url(
                "https://api.affinda.com/v3/documents"
            ),
            "https://api.affinda.com/v3/documents",
        )

    @patch("services.generate_ats_json.requests.post")
    def test_presigned_url_is_sent_directly_to_affinda(self, post_request):
        response = Mock(status_code=201)
        response.json.return_value = {"data": {"candidateName": {}}}
        post_request.return_value = response

        affinda_config = {
            "AFFINDA_API_KEY": "test-token",
            "AFFINDA_WORKSPACE_ID": "test-workspace",
            "AFFINDA_RESUME_DOCUMENT_TYPE_ID": "resume-document-type",
        }
        with patch.multiple("services.generate_ats_json", **affinda_config):
            result = parse_resume_from_s3_url("https://example.com/resume.pdf")

        self.assertEqual(result, response.json.return_value)
        request = post_request.call_args
        self.assertEqual(
            request.kwargs["files"]["url"],
            (None, "https://example.com/resume.pdf"),
        )
        self.assertIn("workspace", request.kwargs["files"])
        self.assertIn("documentType", request.kwargs["files"])
        self.assertEqual(
            request.kwargs["headers"]["Authorization"],
            "Bearer test-token",
        )

    @patch("features.test.parse_resume_from_s3_url")
    @patch("features.test.get_file_url")
    def test_route_returns_only_required_resume_fields(
        self,
        get_file_url,
        parse_resume,
    ):
        get_file_url.return_value = "https://example.com/resume.pdf"
        parse_resume.return_value = {
            "data": {
                "candidateName": {"parsed": {"firstName": "Eiman"}},
                "email": [{"parsed": "candidate@example.com"}],
                "phoneNumber": [{"parsed": {"formattedNumber": "+92 300"}}],
                "location": {"parsed": {"city": "Lahore"}},
                "education": [{"parsed": {}}],
                "workExperience": [{"parsed": {}}],
                "skill": [{"parsed": {"name": "Python"}}],
                "rawText": "must not be returned",
            },
            "meta": {"identifier": "must not be returned"},
        }

        result = test_resume_parser("resumes/candidate/resume.pdf")

        self.assertEqual(
            set(result),
            {
                "candidateName",
                "email",
                "phoneNumber",
                "location",
                "education",
                "workExperience",
                "skill",
            },
        )
        get_file_url.assert_called_once_with("resumes/candidate/resume.pdf")
        parse_resume.assert_called_once_with("https://example.com/resume.pdf")


if __name__ == "__main__":
    unittest.main()
