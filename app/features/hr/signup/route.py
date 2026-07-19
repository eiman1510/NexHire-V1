from fastapi import APIRouter
from models.user import userSignup
from .v1.signup import hr_signup_v1

router = APIRouter(prefix="/auth")


@router.post("/signup/hr", status_code=201)
def hr_signup(user: userSignup):
    return hr_signup_v1(user)
