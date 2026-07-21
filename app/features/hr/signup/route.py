from fastapi import APIRouter
from models.user import userSignup
from dependencies.get_version import load_function

router = APIRouter(prefix="/auth")


@router.post("/signup/hr", status_code=201)
def hr_signup(user: userSignup):
    hr_signup_helper = load_function(
        feature_key="hr:signup",
        module_name="signup",
        function_name="hr_signup_helper",
    )
    return hr_signup_helper(user)
