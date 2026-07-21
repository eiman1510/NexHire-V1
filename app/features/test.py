from fastapi import APIRouter
from services.storage import get_file_url
from services.generate_ats_json import parse_resume_from_s3_url

router = APIRouter()

@router.get("/test_resume_parser")
def test_resume_parser(resume_key: str):

    resume_url = get_file_url(resume_key)
    parsed_resume = parse_resume_from_s3_url(resume_url)

    return {
        "url":resume_url,
        "ats":parsed_resume
    }