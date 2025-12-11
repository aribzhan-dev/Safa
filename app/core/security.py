from passlib.context import CryptContext
import bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:

    if len(password.encode("utf-8")) > 72:
        password = password.encode("utf-8")[:72].decode("utf-8")

    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    if len(password.encode("utf-8")) > 72:
        password = password.encode("utf-8")[:72].decode("utf-8")

    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode())