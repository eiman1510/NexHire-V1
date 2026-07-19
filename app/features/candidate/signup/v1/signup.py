from core.security.password_hashing import hashpass
from core.security.jwt import generate_access_key
from models.user import userSignup, User
from datetime import datetime, timezone
from db_functions.user import find_user, insert_in_user
from utils.response import api_response


def candidatesignup_v1(user: userSignup):

    existing_user = find_user("email", user.email)

    if existing_user:
        return api_response(
            "/routes/signup/candidate", None, "User Already exist", 409, 1
        )

    new_user = User(
        email=user.email,
        username=user.username,
        fullname=user.fullname,
        hash_pass=hashpass(user.password),
        date_joined=datetime.now(timezone.utc),
        role="candidate",
    )

    result = insert_in_user(new_user)
    print(result)
    token = generate_access_key({"id": str(result.inserted_id), "role": "candidate"})

    result = {
        "access_token": token,
        "token_type": "bearer",
        "role": "candidate",
    }

    return api_response(
        status_code=200,
        data=result,
        message="User signed in successfully",
        api_source="Candidate Signup",
    )
