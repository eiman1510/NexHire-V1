from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashpass(password: str):
    return pwd.hash(password)


def verifypass(password: str, hashedpass: str):
    return pwd.verify(password, hashedpass)
