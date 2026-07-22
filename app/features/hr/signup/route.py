from fastapi import APIRouter
from models.user import UserSignup
from .v1.signup import hr_signup_helper

router = APIRouter(prefix="/auth")


@router.post("/signup/hr", status_code=201)
def hr_signup(user: UserSignup):
    return hr_signup_helper(user)
