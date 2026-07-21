import requests
from core.config import RESUME_API_KEY

def parse_resume_from_s3_url(presigned_url: str):

    # Download PDF from S3
    pdf_response = requests.get(presigned_url)

    if pdf_response.status_code != 200:
        raise Exception("Failed to download resume")

    # Send PDF to Resume Parser API
    parser_response = requests.post(
        "https://api.apilayer.com/resume_parser/upload",
        headers={
            "apikey": RESUME_API_KEY,
            "Content-Type": "application/octet-stream"
        },
        data=pdf_response.content
    )

    if parser_response.status_code != 200:
        raise Exception("Resume parsing failed")

    return parser_response.json()