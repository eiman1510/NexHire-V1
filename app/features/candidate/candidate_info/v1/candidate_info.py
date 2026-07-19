from fastapi import UploadFile, File, Form
from services.storage import upload_resume, delete_file
from db_functions.user import update_user, find_user,get_profile_data
from bson import ObjectId
from utils.response import api_response


def submit_candidate_data_v1(
    resume: UploadFile = File(...),
    experience: int = Form(...),
    skills: str = Form(...),
    user=None,
):

    current_user = ObjectId(user["id"])

    key = upload_resume(resume, current_user)

    skills_list = [skill.strip() for skill in skills.split(",")]

    result = update_user(
        current_user,
        {"experience": experience, "skills": skills_list, "resume_key": key},
    )
    if result.matched_count == 0:
        message = "Candidate not found"
    message = "Profile updated"
    print(result)
    return api_response(
        status_code=200, data=None, message=message, api_source="candidate info "
    )


# ----------------------------------------------------------------------------------------


def update_candidate_data_v1(
    resume: UploadFile = File(None),
    experience: int = Form(None),
    skills: str = Form(None),
    current_user=None,
):

    candidate = find_user("_id", ObjectId(current_user["id"]))

    if not candidate:
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

    if skills is not None:
        update_data["skills"] = [skill.strip() for skill in skills.split(",")]

    if resume:
        old_resume = current_user.get("resume_key")
        if old_resume:
            delete_file(old_resume)

        new_resume = upload_resume(resume, current_user["id"])

        update_data["resume_key"] = new_resume

    update_user(current_user["id"], update_data)

    return api_response(
        status_code=200,
        data=None,
        message="Data updated successfully",
        error_code=0,
        api_source="Update candidate info",
    )


def get_user_data_v1(user_id):
    result=get_profile_data(user_id["id"])
    return api_response(status_code=200,data=result,message="User Data retrieved",api_source="Get user in candidate info")