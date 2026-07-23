from fastapi import APIRouter
from services.storage import get_file_url
from services.generate_ats_json import (
    format_resume_data,
    parse_resume_from_s3_url,
)

router = APIRouter()


# @router.get("/test_resume_parser")
# def test_resume_parser(resume_key: str):
#     resume_url = get_file_url(resume_key)
#     parsed_resume = parse_resume_from_s3_url(resume_url)
#     # return format_affinda_resume(parsed_resume)

@router.get("/test_resume_parser")
def test_resume_parser(resume_key: str):
    resume_url = get_file_url(resume_key)

    parsed_resume = parse_resume_from_s3_url(resume_url)
    data=format_resume_data(parsed_resume)
    return data
    # return parsed_resume