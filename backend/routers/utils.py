from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Union, Any


JWT_SECRET_KEY = "32df98f16916857b61a030d50b6d68a3def2bb9699aa33760bb0f3ed99c7ec44"
JWT_REFRESH_SECRET_KEY = (
    "b48d52f4057b87705156e8732ea4a1582b5fc992fb1fdb65bb43c9438dfba54e"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


def create_access_token(subject: Union[str, Any]):
    expires_delta = datetime.now(tz=timezone.utc) + timedelta(
        # minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        seconds=15,
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}

    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(subject: Union[str, Any]):
    expires_delta = datetime.now(tz=timezone.utc) + timedelta(
        minutes=REFRESH_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {"exp": expires_delta, "sub": str(subject)}

    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
