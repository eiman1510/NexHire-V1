from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials,OAuth2PasswordBearer
from jose import jwt
from core.config import SECRET_KEY, ALGORITHM
import re

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return credentials.credentials


def get_auth_type():
    """
    Future:
    jwt, oauth, api_key, etc.
    """
    return "jwt"


# def get_api_version(handler):
#     """
#     Extracts version from imported module path.
#     Example:
#     features.hr.job_handler.v1.job_handler
#     """
#     module = handler.__module__

#     features = {
#         "candidate:apply_job": "v1",
#         "candidate:candidate_info": "v1",
#         "candidate:job_handler": "v1",
#         "candidate:signup": "v1",
#         "hr:application_handler": "v1",
#         "hr:job_handler": "v1",
#         "hr:signup": "v1",
#         "login": "v1",
#     }

#     parts = module.split(".")
#     if parts[:1] == ["features"]:
#         if len(parts) >= 2 and parts[1] == "login":
#             return features.get("login", "unknown")

#         if len(parts) >= 3:
#             feature_key = f"{parts[1]}:{parts[2]}"
#             return features.get(feature_key, "unknown")

#     return "unknown"

def get_user_payload(
    token: str = Depends(get_token)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def get_request_context(paylaod=None):
    """
    Returns everything required by routes.
    """

    def dependency(
        payload=Depends(get_user_payload)
    ):
        return {
            "user": payload,
            "auth_type": get_auth_type(),
            # "api_version": get_api_version(handler)
        }

    return dependency