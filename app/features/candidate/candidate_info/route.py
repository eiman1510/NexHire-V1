from fastapi import APIRouter, UploadFile, File, Form, Depends
from .v1.candidate_info import (
    submit_candidate_data_v1,
    update_candidate_data_v1,
    get_user_data_v1,
)
from dependencies.get_api_content import get_request_context

router = APIRouter()


@router.post("/candidate/info")
def submit_candidate_data(
    resume: UploadFile = File(...),
    experience: int = Form(...),
    skills: str = Form(...),
    context=Depends(get_request_context(submit_candidate_data_v1)),
):
    print(context)
    return submit_candidate_data_v1(resume, experience, skills, context["user"])


# ----------------------------------------------------------------------------------------


@router.put("/candidate/info")
def update_candidate_data(
    resume: UploadFile = File(None),
    experience: int = Form(None),
    skills: str = Form(None),
    context=Depends(get_request_context(update_candidate_data_v1)),
):
    print(context)
    return update_candidate_data_v1(resume, experience, skills, context["user"])


@router.get("/get_Profile_data")
def get_user_data(context=Depends(get_request_context(get_user_data_v1))):
    print(context)
    return get_user_data_v1(context["user"])
