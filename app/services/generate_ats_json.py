import requests

from core.config import (
    AFFINDA_API_KEY,
    AFFINDA_BASE_URL,
    AFFINDA_WORKSPACE_ID,
    AFFINDA_RESUME_DOCUMENT_TYPE_ID,
)
from db_functions.jobs import get_job_by_id
from services.storage import get_file_url

def parse_resume_from_s3_url(presigned_url: str):
    """
    Send S3 resume URL to Affinda and return parsed resume data.
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

    response.raise_for_status()

    return response.json()


def format_resume_data(parser_response):
    """
    Extract ATS-related resume information.
    """

    resume = parser_response.get("data") or {}

    # Skills
    skills = []

    for skill in resume.get("skill") or []:
        parsed = skill.get("parsed") or {}

        skill_name = parsed.get("name")

        if skill_name and skill_name not in skills:
            skills.append(skill_name)

    # Education
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

    # Work Experience
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

    # Email
    emails = resume.get("email") or []

    email = None
    if emails:
        email = emails[0].get("parsed")

    # Phone Number
    phone_numbers = resume.get("phoneNumber") or []

    phone = None
    if phone_numbers:
        phone = (phone_numbers[0].get("parsed") or {}).get(
            "formattedNumber"
        )

    return {
        "candidateName": (
            (resume.get("candidateName") or {})
            .get("raw")
        ),
        "email": email,
        "phoneNumber": phone,
        "location": resume.get("location"),
        "skills": skills,
        "education": education,
        "workExperience": experience,
    }

def resume_parser(resume_key: str):
    resume_url = get_file_url(resume_key)

    parsed_resume = parse_resume_from_s3_url(resume_url)
    data=format_resume_data(parsed_resume)
    return data

def calculate_ats_score(
    parsed_resume: dict,
    job_id: str,
):
   

    job = get_job_by_id(job_id)

    if job is None:
        raise ValueError(f"Job with ID {job_id} was not found")

    threshold = job.get("threshold")

    # Jobs created before the threshold field was added use 50%.
    if threshold is None:
        threshold = 50.0

    candidate_skills = set(
        skill.lower()
        for skill in parsed_resume.get("skills", [])
    )

    required_skills = set(
        skill.lower()
        for skill in job.get(
            "required_skills",
            job.get("skills_required", []),
        )
    )

    candidate_education = ""

    education = parsed_resume.get("education", [])

    if education:
        candidate_education = (
            education[0].get("degree") or ""
        ).lower()

    required_education = (
        job.get("minimum_education") or ""
    ).lower()

    # Skill Matching
    matched_skills = candidate_skills.intersection(
        required_skills
    )

    ats_score = 0

    if required_skills:
        ats_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 100

    skill_check = 1 if ats_score >= threshold else 0

    # Education Matching
    education_check = (
        1
        if required_education in candidate_education
        else 0
    )

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
