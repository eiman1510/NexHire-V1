from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import jwt
from core.config import SECRET_KEY, ALGORITHM

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return credentials.credentials


def get_auth_type():
    """
    Future:
    jwt, oauth, api_key, etc.
    """
    return "jwt"


def get_user_payload(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_request_context():
    """
    Returns everything required by routes.
    """

    def dependency(payload=Depends(get_user_payload)):
        return {
            "user": payload,
            "auth_type": get_auth_type(),
        }


    return dependency
