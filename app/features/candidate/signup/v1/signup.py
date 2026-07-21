from core.security.password_hashing import hashpass
from core.security.jwt import generate_access_key
from models.user import userSignup, User
from datetime import datetime, timezone
from db_functions.user import find_user, insert_in_user
from utils.response import api_response
from logging_config import logger


def candidatesignup_helper(user: userSignup):
    try:
        logger.info(f"Candidate signup attempt for email: {user.email}")

        existing_user = find_user("email", user.email)

        if existing_user:
            logger.warning(f"Signup failed. User already exists: {user.email}")

            return api_response(
                status_code=409,
                data=None,
                message="User Already exist",
                api_source="/routes/signup/candidate",
                error_code=1,
            )

        logger.info(f"Hashing password for candidate: {user.email}")

        new_user = User(
            email=user.email,
            username=user.username,
            fullname=user.fullname,
            hash_pass=hashpass(user.password),
            date_joined=datetime.now(timezone.utc),
            role="candidate",
        )

        logger.info(f"Creating candidate account for: {user.email}")

        db_result = insert_in_user(new_user)

        logger.info(f"Candidate created successfully with id: {db_result.inserted_id}")

        token = generate_access_key(
            {
                "id": str(db_result.inserted_id),
                "role": "candidate",
            }
        )

        logger.info(f"Access token generated for candidate: {user.email}")

        response_data = {
            "access_token": token,
            "token_type": "bearer",
            "role": "candidate",
        }

        return api_response(
            status_code=200,
            data=response_data,
            message="User signed in successfully",
            api_source="Candidate Signup",
        )

    except Exception:
        logger.exception(f"Unexpected error during candidate signup for: {user.email}")

        return api_response(
            status_code=500,
            data=None,
            message="Internal Server Error",
            api_source="Candidate Signup",
            error_code=1,
        )
