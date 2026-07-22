from fastapi import APIRouter
from db_functions.user import find_user_by_field
from models.user import UserLogin
from core.security.password_hashing import verify_password
from core.security.jwt import generate_access_key
from utils.response import api_response
from logging_config import logger

router = APIRouter(prefix="/auth")


@router.post("/login")
def login(user: UserLogin):
    try:
        logger.info(f"Login attempt for email: {user.email}")

        stored_user = find_user_by_field("email", user.email)

        if not stored_user:
            logger.warning(f"User not found: {user.email}")

            return api_response(
                status_code=409,
                data=None,
                message="User not found",
                api_source="Login",
                error_code=1,
            )

        logger.info(f"User found: {user.email}")

        if not verify_password(user.password, stored_user["hash_pass"]):
            logger.warning(f"Invalid password for user: {user.email}")

            return api_response(
                status_code=401,
                data=None,
                message="Invalid credentials",
                api_source="Login",
                error_code=1,
            )

        logger.info(f"Password verified for user: {user.email}")

        token = generate_access_key(
            {"id": str(stored_user["_id"]), "role": stored_user["role"]}
        )

        logger.info(f"Access token generated for user: {user.email}")

        result = {
            "access_key": token,
            "token_type": "bearer",
            "role": stored_user["role"],
        }

        logger.info(f"Login successful for user: {user.email}")

        return api_response(
            status_code=200,
            data=result,
            message="Logged in Successfully",
            api_source="Login",
        )

    except Exception:
        logger.exception(f"Unexpected error during login for user: {user.email}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Login",
            error_code=1,
        )
