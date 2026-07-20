from fastapi import APIRouter, UploadFile, File, Form, Depends
from .v1.candidate_info import (
    submit_candidate_data_v1,
    update_candidate_data_v1,
    get_user_data_v1,
)
from dependencies.get_user import get_current_user

router = APIRouter()


@router.post("/candidate/info")
def submit_candidate_data(
    resume: UploadFile = File(...),
    experience: int = Form(...),
    skills: str = Form(...),
    user=Depends(get_current_user),
):

    return submit_candidate_data_v1(resume, experience, skills, user)


# ----------------------------------------------------------------------------------------


@router.put("/candidate/info")
def update_candidate_data(
    resume: UploadFile = File(None),
    experience: int = Form(None),
    skills: str = Form(None),
    user=Depends(get_current_user),
):
    return update_candidate_data_v1(resume, experience, skills, user)


@router.get("/get_Profile_data")
def get_user_data(user=Depends(get_current_user)):
    return get_user_data_v1(user)
