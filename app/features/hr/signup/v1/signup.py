from core.security.password_hashing import hashpass
from core.security.jwt import generate_access_key
from models.user import userSignup, User
from datetime import datetime, timezone
from db_functions.user import (
    find_user,
    insert_in_user,
    find_email_in_admin,
    update_admin,
)
from utils.response import api_response
from logging_config import logger


def hr_signup_helper(user: userSignup):
    try:
        admin_approved = find_email_in_admin(user.email)

        if not admin_approved:
            logger.warning(f"This email is not authorized for Hr Signup: {user.email}")
            return api_response(
                status_code=403,
                data=None,
                message="Email not recognized as HR",
                api_source="hr signup",
                error_code=1,
            )

        if admin_approved["registered"]:
            logger.info(f"Hr Email already exists: {user.email}")
            return api_response(
                status_code=403,
                data=None,
                message="Hr Email already registered",
                api_source="hr signup",
                error_code=1,
            )

        existing_user = find_user("email", user.email)

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
            hash_pass=hashpass(user.password),
            date_joined=datetime.now(timezone.utc),
            role="hr",
        )

        db_user = insert_in_user(new_user)

        logger.info(f"HR created successfully with id: {db_user.inserted_id}")

        update_admin(email=user.email, update_data={"registered": True})

        token = generate_access_key({"id": str(db_user.inserted_id), "role": "hr"})

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
    except:
        logger.exception(f"Unexpected error during candidate signup for: {user.email}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Hr Signup",
            error_code=1,
        )
