from core.security.password_hashing import hash_password
from core.security.jwt import generate_access_key
from models.user import User, UserSignup
from datetime import datetime, timezone
from db_functions.user import (
    create_user,
    find_allowed_hr_by_email,
    find_user_by_field,
    update_allowed_hr_by_email,
)
from utils.response import api_response
from logging_config import logger


def hr_signup_helper(user: UserSignup):
    try:
        allowed_hr = find_allowed_hr_by_email(user.email)

        if not allowed_hr:
            logger.warning(f"This email is not authorized for Hr Signup: {user.email}")
            return api_response(
                status_code=403,
                data=None,
                message="Email not recognized as HR",
                api_source="hr signup",
                error_code=1,
            )

        if allowed_hr["registered"]:
            logger.info(f"Hr Email already exists: {user.email}")
            return api_response(
                status_code=403,
                data=None,
                message="Hr Email already registered",
                api_source="hr signup",
                error_code=1,
            )

        existing_user = find_user_by_field("email", user.email)

        if existing_user:
            logger.warning(f"Signup failed. User already exists: {user.email}")
            return api_response(
                status_code=409,
                data=None,
                message="User with thie mail already exist",
                api_source="hr signup",
                error_code=1,
            )

        new_user = User(
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            hash_pass=hash_password(user.password),
            date_joined=datetime.now(timezone.utc),
            role="hr",
        )

        insert_result = create_user(new_user)

        logger.info(f"HR created successfully with id: {insert_result.inserted_id}")

        update_allowed_hr_by_email(email=user.email, update_data={"registered": True})

        token = generate_access_key(
            {"id": str(insert_result.inserted_id), "role": "hr"}
        )

        logger.info(f"Access token generated for candidate: {user.email}")
        result = {
            "access_token": token,
            "token_type": "bearer",
            "role": "hr",
        }
        return api_response(
            status_code=200,
            data=result,
            message="HR user created successfully",
            api_source="hr signup",
        )
    except Exception:
        logger.exception(f"Unexpected error during HR signup for: {user.email}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Hr Signup",
            error_code=1,
        )
