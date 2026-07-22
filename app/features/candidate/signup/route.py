from fastapi import APIRouter
from models.user import UserSignup
from .v1.signup import candidate_signup_helper

router = APIRouter(prefix="/auth")


@router.post("/signup/candidate", status_code=201)
def candidate_signup(user: UserSignup):
    return candidate_signup_helper(user)
