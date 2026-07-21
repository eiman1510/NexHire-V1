from fastapi import APIRouter, UploadFile, File, Form, Depends
from dependencies.get_api_content import get_request_context
from dependencies.get_version import load_function

router = APIRouter()


@router.post("/candidate/info")
def submit_candidate_data(
    resume: UploadFile = File(...),
    experience: int = Form(...),
    skills: str = Form(...),
    context=Depends(get_request_context()),
):
    print(context)
    submit_candidate_data_helper = load_function(
        feature_key="candidate:candidate_info",
        module_name="candidate_info",
        function_name="submit_candidate_data_helper",
    )
    return submit_candidate_data_helper(resume, experience, skills, context["user"])


# ----------------------------------------------------------------------------------------


@router.put("/candidate/info")
def update_candidate_data(
    resume: UploadFile = File(None),
    experience: int = Form(None),
    skills: str = Form(None),
    context=Depends(get_request_context()),
):
    print(context)
    update_candidate_data_helper = load_function(
        feature_key="candidate:candidate_info",
        module_name="candidate_info",
        function_name="update_candidate_data_helper",
    )
    return update_candidate_data_helper(resume, experience, skills, context["user"])


@router.get("/get_Profile_data")
def get_user_data(context=Depends(get_request_context())):
    print(context)
    get_user_data_helper = load_function(
        feature_key="candidate:candidate_info",
        module_name="candidate_info",
        function_name="get_user_data_helper",
    )
    return get_user_data_helper(context["user"])
