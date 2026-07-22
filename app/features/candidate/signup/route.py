from fastapi import APIRouter
from models.user import userSignup
from .v1.signup import candidatesignup_helper

router = APIRouter(prefix="/auth")


@router.post("/signup/candidate", status_code=201)
def candidatesignup(user: userSignup):
    return candidatesignup_helper(user)
