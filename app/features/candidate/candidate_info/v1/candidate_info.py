from fastapi import UploadFile, File, Form
from services.storage import upload_resume, delete_file
from db_functions.user import (
    find_user_by_field,
    get_user_profile_by_id,
    update_user_by_id,
)
from bson import ObjectId
from utils.response import api_response
from logging_config import logger

# ----------------------------------------------------------------------------------------
# CANDIDATE FUNCTION
# Submit candidate profile information(resume,experience,skills)
# ----------------------------------------------------------------------------------------


def submit_candidate_data_helper(
    resume: UploadFile = File(...),
    experience: int = Form(...),
    skills: str = Form(...),
    user=None,
):
    try:
        current_user = ObjectId(user["id"])

        logger.info(f"Candidate {current_user} started profile submission")

        try:
            key = upload_resume(resume, current_user)

            logger.info(f"Resume uploaded successfully for candidate {current_user}")

        except Exception:
            logger.exception(f"Resume upload failed for candidate {current_user}")
            raise

        skills_list = [skill.strip() for skill in skills.split(",")]

        result = update_user_by_id(
            current_user,
            {
                "experience": experience,
                "skills": skills_list,
                "resume_key": key,
            },
        )

        if result.matched_count == 0:
            logger.warning(f"Candidate not found during profile update: {current_user}")

            return api_response(
                status_code=404,
                data=None,
                message="Candidate not found",
                api_source="candidate info",
                error_code=1,
            )

        logger.info(f"Profile updated successfully for candidate {current_user}")

        return api_response(
            status_code=200,
            data=None,
            message="Profile updated",
            api_source="candidate info",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while submitting profile for user {user.get('id')}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="candidate info",
            error_code=1,
        )


# ----------------------------------------------------------------------------------------
# CANDIDATE FUNCTION
# Update candidate profile information
# ----------------------------------------------------------------------------------------


def update_candidate_data_helper(
    resume: UploadFile = File(None),
    experience: int = Form(None),
    skills: str = Form(None),
    current_user=None,
):
    try:
        candidate_id = current_user["id"]

        logger.info(f"Candidate {candidate_id} requested profile update")

        candidate = find_user_by_field("_id", ObjectId(candidate_id))

        if not candidate:
            logger.warning(f"Candidate not found during update: {candidate_id}")

            return api_response(
                status_code=409,
                data=None,
                message="User not found",
                error_code=1,
                api_source="Update candidate info",
            )

        update_data = {}

        if experience is not None:
            update_data["experience"] = experience
            logger.info(f"Experience updated for candidate {candidate_id}")

        if skills is not None:
            update_data["skills"] = [skill.strip() for skill in skills.split(",")]
            logger.info(f"Skills updated for candidate {candidate_id}")

        if resume:
            logger.info(f"Resume update started for candidate {candidate_id}")

            try:
                old_resume = candidate.get("resume_key")

                if old_resume:
                    delete_file(old_resume)

                    logger.info(f"Old resume deleted for candidate {candidate_id}")

                new_resume = upload_resume(resume, candidate_id)

                logger.info(
                    f"New resume uploaded successfully for candidate {candidate_id}"
                )

                update_data["resume_key"] = new_resume

            except Exception:
                logger.exception(f"Resume update failed for candidate {candidate_id}")
                raise

        update_user_by_id(candidate_id, update_data)

        logger.info(f"Profile updated successfully for candidate {candidate_id}")

        return api_response(
            status_code=200,
            data=None,
            message="Data updated successfully",
            error_code=0,
            api_source="Update candidate info",
        )

    except Exception:
        logger.exception(
            f"Unexpected error while updating profile for user {current_user}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Update candidate info",
            error_code=1,
        )


# ----------------------------------------------------------------------------------------
# CANDIDATE FUNCTION
# Get candidate profile information
# ----------------------------------------------------------------------------------------


def get_user_data_helper(user_id):
    try:
        logger.info(f"Fetching profile data for candidate {user_id['id']}")

        result = get_user_profile_by_id(user_id["id"])

        logger.info(f"Profile data fetched successfully for candidate {user_id['id']}")

        return api_response(
            status_code=200,
            data=result,
            message="User Data retrieved",
            api_source="Get user in candidate info",
        )

    except Exception:
        logger.exception(
            f"Error fetching profile data for candidate {user_id.get('id')}"
        )

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Get user in candidate info",
            error_code=1,
        )
