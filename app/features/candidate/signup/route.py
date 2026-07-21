from fastapi import APIRouter
from models.user import userSignup
from dependencies.get_version import load_function

router = APIRouter(prefix="/auth")


@router.post("/signup/candidate", status_code=201)
def candidatesignup(user: userSignup):
    candidatesignup_helper = load_function(
        feature_key="candidate:signup",
        module_name="signup",
        function_name="candidatesignup_helper",
    )
    return candidatesignup_helper(user)
