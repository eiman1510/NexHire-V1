import requests

from core.config import (
    AFFINDA_API_KEY,
    AFFINDA_BASE_URL,
    AFFINDA_WORKSPACE_ID,
    AFFINDA_RESUME_DOCUMENT_TYPE_ID,
)
from db_functions.jobs import get_job_by_id
from services.education_matching import education_matches
from services.storage import get_file_url


def parse_resume_from_s3_url(presigned_url: str):
    """
    Sends the S3 resume URL to Affinda API and returns the parsed resume data.
    """

    response = requests.post(
        f"{AFFINDA_BASE_URL.rstrip('/')}/v3/documents",
        headers={
            "Authorization": f"Bearer {AFFINDA_API_KEY}"
        },
        files={
            "url": (None, presigned_url),
            "workspace": (None, AFFINDA_WORKSPACE_ID),
            "documentType": (None, AFFINDA_RESUME_DOCUMENT_TYPE_ID),
        },
        timeout=120,
    )

    # Raise an error if the request fails
    response.raise_for_status()

    return response.json()


def format_resume_data(parser_response):
    """
    Extracts only the ATS-related information from Affinda's response.
    """

    resume = parser_response.get("data") or {}

    # Extract unique skills
    skills = []

    for skill in resume.get("skill") or []:
        skill_name = (skill.get("parsed") or {}).get("name")

        if skill_name and skill_name not in skills:
            skills.append(skill_name)

    # Extract education details
    education = []

    for edu in resume.get("education") or []:
        parsed = edu.get("parsed") or {}

        education.append(
            {
                "degree": (
                    (parsed.get("educationAccreditation") or {})
                    .get("parsed")
                ),
                "institution": (
                    (parsed.get("educationOrganization") or {})
                    .get("parsed")
                ),
            }
        )

    # Extract work experience
    experience = []

    for exp in resume.get("workExperience") or []:
        parsed = exp.get("parsed") or {}

        experience.append(
            {
                "jobTitle": (
                    (parsed.get("workExperienceJobTitle") or {})
                    .get("parsed")
                ),
                "company": (
                    (parsed.get("workExperienceOrganization") or {})
                    .get("parsed")
                ),
            }
        )

    # Get the first email if available
    emails = resume.get("email") or []
    email = emails[0].get("parsed") if emails else None

    # Get the first phone number if available
    phone_numbers = resume.get("phoneNumber") or []
    phone = (
        (phone_numbers[0].get("parsed") or {}).get("formattedNumber")
        if phone_numbers
        else None
    )

    return {
        "candidateName": (resume.get("candidateName") or {}).get("raw"),
        "email": email,
        "phoneNumber": phone,
        "location": resume.get("location"),
        "skills": skills,
        "education": education,
        "workExperience": experience,
    }


def resume_parser(resume_key: str):
    """
    Gets the resume from S3, sends it to Affinda, and returns formatted data.
    """

    resume_url = get_file_url(resume_key)

    parsed_resume = parse_resume_from_s3_url(resume_url)

    return format_resume_data(parsed_resume)


def calculate_ats_score(parsed_resume: dict, job_id: str):
    """
    Calculates the ATS score by comparing candidate skills and education
    with the job requirements.
    """

    # Get job details from the database
    job = get_job_by_id(job_id)

    if job is None:
        raise ValueError(f"Job with ID {job_id} was not found")

    # Use 50% if threshold is missing (older jobs)
    threshold = job.get("threshold")
    if threshold is None:
        threshold = 50.0

    # Convert candidate skills to lowercase for comparison
    candidate_skills = {
        skill.lower()
        for skill in parsed_resume.get("skills", [])
    }

    # Convert required skills to lowercase for comparison
    required_skills = {
        skill.lower()
        for skill in job.get(
            "required_skills",
            job.get("skills_required", []),
        )
    }

    # Get candidate degrees
    candidate_degrees = [
        entry.get("degree")
        for entry in parsed_resume.get("education", [])
        if isinstance(entry, dict) and entry.get("degree")
    ]

    required_education = job.get("minimum_education") or ""

    # Find matching skills
    matched_skills = candidate_skills.intersection(required_skills)

    # Calculate ATS score based on matched skills
    ats_score = 0

    if required_skills:
        ats_score = (
            len(matched_skills) / len(required_skills)
        ) * 100

    # Check if skill score meets the threshold
    skill_check = int(ats_score >= threshold)

    # Check if education requirement is met
    education_check = int(
        education_matches(
            required_education,
            candidate_degrees,
        )
    )

    # Candidate is selected only if both checks pass
    selected = (
        skill_check == 1
        and education_check == 1
    )

    return {
        "ats_score": round(ats_score, 2),
        "matched_skills": list(matched_skills),
        "education_match": education_check,
        "selected": selected,
    }