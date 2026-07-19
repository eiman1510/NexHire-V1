from fastapi import APIRouter
from db_functions.user import find_user
from models.user import UserLogin
from core.security.password_hashing import verifypass
from core.security.jwt import generate_access_key
from utils.response import api_response

router = APIRouter(prefix="/auth")


@router.post("/login")
def login(user: UserLogin):

    db_user = find_user("email", user.email)
    if not db_user:
        return api_response(
            status_code=409,
            data=None,
            message="User not found",
            api_source="Login",
            error_code=1,
        )

    if not verifypass(user.password, db_user["hash_pass"]):
        return api_response(
            status_code=401,
            data=None,
            message="Invalid credentials",
            api_source="Login",
            error_code=1,
        )

    token = generate_access_key({"id": str(db_user["_id"]), "role": db_user["role"]})

    result = {"access_key": token, "token_type": "bearer", "role": db_user["role"]}
    return api_response(
        status_code=200,
        data=result,
        message="Logged in Successfully",
        api_source="Login",
    )
