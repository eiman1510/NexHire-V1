from jose import jwt
from datetime import datetime, timedelta, timezone
from core.config import SECRET_KEY, ALGORITHM


def generate_access_key(data: dict):
    print("SECRET_KEY =", SECRET_KEY)
    print("ALGORITHM =", ALGORITHM)
    payload = data.copy()
    payload.update({"exp": datetime.now(timezone.utc) + timedelta(hours=1)})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    print("Token created", token)
    return token
